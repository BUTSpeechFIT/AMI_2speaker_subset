#!/bin/bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
OUTDIR=$DIR/2spk_subsets
AMIWAVSDIR=/mnt/matylda4/landini/data/AMI/wavs
KALDI_UTILS_DIR=/mnt/matylda5/lozano/exp2019/DIHARD2020/E2E_EDA/EEND/egs/callhome/v1

REC_TYPE=".Headset-" # ".Headset-" or ".Array1-"

for SET in dev test train; do
    python $DIR/generate_recordings.py $DIR/speaker_pairs_lists/$SET.txt $DIR/mapping_speakers_channels.txt $AMIWAVSDIR/$SET $DIR/AMI-diarization-setup/only_words/rttms/$SET $OUTDIR/wavs/$SET $OUTDIR/rttms/$SET 16000 $REC_TYPE

    bash prepare_data_dir.sh $KALDI_UTILS_DIR $OUTDIR/wavs/$SET $OUTDIR/rttms/$SET $DIR/speaker_pairs_lists/$SET.txt $OUTDIR/data/$SET
done

