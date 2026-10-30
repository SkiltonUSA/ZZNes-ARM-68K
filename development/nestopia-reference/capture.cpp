// Offline reference capture. No Amiga hardware or installed files are touched.
#include "api/NstApiEmulator.hpp"
#include "api/NstApiMachine.hpp"
#include "api/NstApiSound.hpp"
#include "api/NstApiVideo.hpp"
#include "api/NstApiInput.hpp"
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <vector>
#include <stdexcept>
#include <string>

static FILE* trace;
static unsigned capture_frame;
void reference_apu_write(unsigned long cycle, unsigned address, unsigned value) {
    if (trace) std::fprintf(trace, "%u,%lu,%u,%u\n", capture_frame, cycle, address, value);
}

static void check(Nes::Result result, const char* operation) {
    if (result < 0) throw std::runtime_error(operation);
}

int main(int argc, char** argv) {
    if (argc != 7) {
        std::fprintf(stderr, "capture ROM OUTPUT_PREFIX FRAMES RATE FILTER POP_REDUCER\n");
        return 2;
    }
    try {
        const int frames = std::atoi(argv[3]);
        const int rate = std::atoi(argv[4]);
        if (frames < 1 || rate < 8000 || rate > 96000)
            throw std::runtime_error("invalid frame count/rate");
        const std::string prefix(argv[2]);
        if (std::getenv("NESTOPIA_APU_TRACE")) {
            trace = std::fopen((prefix + ".apu.csv").c_str(), "w");
            if (!trace) throw std::runtime_error("open APU trace");
            std::fprintf(trace, "frame,cycle,address,value\n");
        }
        std::ifstream rom(argv[1], std::ios::binary);
        if (!rom) throw std::runtime_error("open ROM");
        std::ofstream pcm((prefix + ".pcm").c_str(), std::ios::binary);
        std::ofstream counts((prefix + ".csv").c_str());
        if (!pcm || !counts) throw std::runtime_error("open output");
        Nes::Api::Emulator emulator;
        Nes::Api::Machine machine(emulator);
        Nes::Api::Sound sound(emulator);
        Nes::Api::Video video(emulator);
        check(machine.Load(rom, Nes::Api::Machine::FAVORED_NES_NTSC), "load ROM");
        check(machine.SetMode(Nes::Api::Machine::NTSC), "NTSC");
        check(sound.SetSampleRate(rate), "sample rate");
        check(sound.SetVolume(Nes::Api::Sound::ALL_CHANNELS, 100), "volume");
        check(sound.SetSpeed(Nes::Api::Sound::DEFAULT_SPEED), "speed");
        sound.SetFilter(std::atoi(argv[5]) != 0);
        sound.SetDmcPopReducer(std::atoi(argv[6]) != 0);
        Nes::Api::Video::RenderState render;
        render.width = 256; render.height = 240;
        render.bits.count = 32;
        render.bits.mask.r = 0xff0000;
        render.bits.mask.g = 0x00ff00;
        render.bits.mask.b = 0x0000ff;
        check(video.SetRenderState(render), "render state");
        check(machine.Power(true), "power on");
        std::vector<unsigned int> pixels(256 * 240);
        std::vector<short> samples(4096);
        Nes::Api::Video::Output picture(&pixels[0], 256 * 4);
        Nes::Core::Input::Controllers input;
        counts << "frame,samples,video_fnv1a\n";
        unsigned long long total = 0;
        for (int frame = 0; frame < frames; ++frame) {
            capture_frame = frame + 1;
            Nes::Api::Sound::Output output(&samples[0], samples.size());
            check(emulator.Execute(&picture, &output, &input), "execute");
            if (output.length[0] > samples.size()) throw std::runtime_error("audio bounds");
            for (unsigned i = 0; i < output.length[0]; ++i) {
                unsigned short v = static_cast<unsigned short>(samples[i]);
                pcm.put(v & 255); pcm.put(v >> 8);
            }
            unsigned int hash = 2166136261u;
            for (unsigned i = 0; i < pixels.size(); ++i) hash = (hash ^ pixels[i]) * 16777619u;
            total += output.length[0];
            counts << frame + 1 << ',' << output.length[0] << ',' << hash << '\n';
            if ((frame + 1) % 300 == 0 || frame + 1 == frames) {
                char suffix[32]; std::snprintf(suffix, sizeof(suffix), "-%04d.ppm", frame + 1);
                std::ofstream image((prefix + suffix).c_str(), std::ios::binary);
                image << "P6\n256 240\n255\n";
                for (unsigned i = 0; i < pixels.size(); ++i) {
                    image.put((pixels[i] >> 16) & 255);
                    image.put((pixels[i] >> 8) & 255);
                    image.put(pixels[i] & 255);
                }
            }
        }
        check(machine.Power(false), "power off");
        pcm.close(); counts.close();
        if (trace) { std::fclose(trace); trace = 0; }
        if (!pcm || !counts) throw std::runtime_error("write output");
        std::printf("PASS frames=%d samples=%llu rate=%d filter=%s pop=%s\n",
                    frames, total, rate, argv[5], argv[6]);
    } catch (const std::exception& e) {
        std::fprintf(stderr, "FAIL %s\n", e.what()); return 1;
    }
}
