"""NES-only native-column display option; keep archived inputs unchanged."""
from prepare_output_quality import edit

def prepare_launcher(lib):
 edit(lib/'library_mui.h','"Sharp pixels","Smooth scrolling",NULL','"Sharp pixels","Smooth scrolling","Native columns",NULL')
 edit(lib/'library_mui.h','Smooth horizontal scaling reduces uneven pixel columns during scrolling.\\nSharp preserves hard pixel edges. Smooth adds ARM processing work.','Native: 256 equal-width columns with side borders; narrower picture.\\nSharp/Smooth retain monitor aspect correction. Edge masks still apply.')
 edit(lib/'library_mui.h','The game keeps a physical 4:3 shape.','Native keeps equal columns; Sharp/Smooth keep 4:3.')
 edit(lib/'ui_model.h','m->smooth>1','m->smooth>2')

def prepare_player(stage):
 p=stage/'view.h'
 edit(p,'horizontal linear filter[8].','horizontal scale[8..9]: Sharp=0, Smooth=1, Native=2.')
 edit(p,'return opt<512 &&','return opt<768 &&')
 edit(p,'return (opt&1)?240:320;','return (opt&512)?256:(opt&1)?240:320;')
 edit(p,'sx=(opt&1)?(x-left)*16/15:(x-left)*4/5;','sx=(opt&512)?x-left:(opt&1)?(x-left)*16/15:(x-left)*4/5;')
 edit(stage/'session.h','fc_view>=512','fc_view>=768')
