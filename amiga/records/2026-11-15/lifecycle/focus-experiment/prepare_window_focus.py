"""Restore player keyboard focus after Intuition finishes a screen-depth change."""
def prepare(stage):
    def edit(name,before,after):
        path=stage/name
        text=path.read_text()
        if text.count(before)!=1:
            raise ValueError(f'{name}: expected one window-focus patch anchor')
        path.write_text(text.replace(before,after))
    edit('host.c','static int em_switch_pending,em_ready;',
         'static int em_switch_pending,em_ready,em_focus_pending;\nstatic ULONG em_focus_due;')
    edit('host.c',' if(!window)return;\n while((msg=',
         ' if(!window)return;\n /* Screen-depth work can overwrite immediate window activation. */\n'
         ' if(em_focus_pending&&(LONG)(us()-em_focus_due)>=0){ActivateWindow(window);em_focus_pending=0;}\n'
         ' while((msg=')
    edit('window_display.h','static void em_display_close(void){',
         'static void em_display_close(void){\n em_focus_pending=0;')
    edit('window_display.h','next_frame_us=0;fc_last_flip=0;return full_open();',
         'next_frame_us=0;fc_last_flip=0;\n int opened=full_open();\n'
         ' if(opened&&fc_windowed){em_focus_due=us()+100000u;em_focus_pending=1;}\n'
         ' return opened;')
