import pathlib

import sys
sys.path.append('../../')

import LexicalDataD2TAnnotationTool
from LexicalDataD2TAnnotationTool import initialize_typical_frames
from LexicalDataD2TAnnotationTool import update_typical_frames
from LexicalDataD2TAnnotationTool import create_lexical_lookup_per_eventtype

from nltk.corpus import framenet as fn


cwd = pathlib.Path.cwd()
parent = cwd.parent

out_dir = f'{parent}/test/lexicon_data_for_frame_annotation_tool'
premon_nt_path = f'{parent}/res/premon/premon-2018a-fn17-noinf.nt'


initialize_typical_frames(output_folder=out_dir,
                          fn_en=fn,
                          premon=LexicalDataD2TAnnotationTool.premon,
                          event_type='Q40231',
                          overwrite=True,
                          verbose=2)


frame_to_typicality = {
    'Change_of_leadership' : 0.6,
    'Appointing' : 0.4
}

update_typical_frames(output_folder=out_dir,
                      premon=LexicalDataD2TAnnotationTool.premon,
                      event_type='Q40231',
                      frame_to_typicality=frame_to_typicality,
                      frame_format='fn_label',
                      verbose=2)

frame_to_typicality = {
    'http://premon.fbk.eu/resource/fn17-change_of_leadership' : 0.8,
}

update_typical_frames(output_folder=out_dir,
                      premon=LexicalDataD2TAnnotationTool.premon,
                      event_type='Q40231',
                      frame_to_typicality=frame_to_typicality,
                      frame_format='premon_frame_uri',
                      verbose=2)


create_lexical_lookup_per_eventtype(event_type='Q40231',
                                    language='nl',
                                    premon=LexicalDataD2TAnnotationTool.premon,
                                    output_folder=out_dir,
                                    overwrite=True,
                                    verbose=2)

create_lexical_lookup_per_eventtype(event_type='Q40231',
                                    language='en',
                                    premon=LexicalDataD2TAnnotationTool.premon,
                                    output_folder=out_dir,
                                    overwrite=True,
                                    verbose=2)
