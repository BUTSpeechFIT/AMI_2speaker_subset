#!/usr/bin/env python
import numpy as np
from optparse import OptionParser
import os
from scipy.io import wavfile
from diarization_utils.rttm_utils import hard_labels_to_rttm, rttm_to_hard_labels


def main():
    usage = "%prog [options] txt_list, channels_mapping, wavs_dir, \
             rttms_dir, out_wav_dir, out_rttm_dir, \
             sampling_frequency, rec_type"
    desc = "Compute stats about segments in the set."
    parser = OptionParser(usage=usage, description=desc)
    (opt, args) = parser.parse_args()
    if (len(args) != 8):
        parser.error("Incorrect number of arguments")
    (
        txt_list,
        channels_mapping,
        wavs_dir,
        rttms_dir,
        out_wav_dir,
        out_rttm_dir,
        sampling_frequency,
        rec_type
    ) = args
    sampling_frequency = float(sampling_frequency)
    pairs = [line.rstrip() for line in open(txt_list, 'r')]

    mappings_list = [line.rstrip() for line in open(channels_mapping, 'r')]
    mappings = {}
    for m in mappings_list:
        utt_id = m.split()[0]
        channel = m.split()[1]
        spk_id = m.split()[2]
        if not (utt_id in mappings):
            mappings[utt_id] = {}
        mappings[utt_id][spk_id] = channel

    names = {}
    pair2utt = {}
    for p in pairs:
        utt_id = p.split('_')[0]
        spk_ids = p.split('_')[1:]
        names[p] = spk_ids
        pair2utt[p] = utt_id

    if not os.path.exists(out_wav_dir):
        os.makedirs(out_wav_dir)

    precision = 1000

    for p in pairs:
        if not os.path.isfile(os.path.join(out_wav_dir, p+'.wav')):
            print('Processing: '+p)
            utt_id = p.split('_')[0]
            spk1 = p.split('_')[1]
            spk2 = p.split('_')[2]
            rttm_matrix, rttm_labels = rttm_to_hard_labels(os.path.join(
                rttms_dir, f"{utt_id}.rttm"), precision)

            mask = np.ones(rttm_matrix.shape[0])
            wanted_spks = np.where((rttm_labels == spk1) | (rttm_labels == spk2))[0]
            unwanted_spks = np.where((rttm_labels != spk1) & (rttm_labels != spk2))[0]
            new_rttm_labels = rttm_labels[wanted_spks]
            mask[np.where(rttm_matrix[:, unwanted_spks].sum(axis=1) > 0)[0]] = 0
            new_rttm_matrix = rttm_matrix[mask.astype(bool), :]
            new_rttm_matrix = new_rttm_matrix[:, wanted_spks]
            hard_labels_to_rttm(new_rttm_matrix, new_rttm_labels, p,
                                os.path.join(out_rttm_dir, f"{p}.rttm"), precision)

            mask_extended = np.concatenate((np.zeros(1), mask, np.zeros(1)), axis=0)
            changes = np.where(
               mask_extended[1:] - mask_extended[:-1]
            )[0].astype(float)
            if changes[-1] == mask.shape[0]:
                changes[-1] -= 1  # avoid reading out of array
            beg = changes[:-1]
            end = changes[1:]
            # So far, beg and end include the segments we want to keep in between
            beg_audio = beg[1::2]
            end_audio = end[1::2]
            assert beg_audio.shape[0] == end_audio.shape[0], \
                   "Amount of beginning and end of segments do not match."
            first = True
            for spk in names[p]:
                _, data = wavfile.read(os.path.join(wavs_dir,
                                       pair2utt[p] + rec_type +
                                       mappings[pair2utt[p]][spk]+'.wav'))
                audio_mask = np.ones(data.shape)
                for s in range(beg_audio.shape[0]):
                    beg_audio_index = int(beg_audio[s]/precision*sampling_frequency)
                    end_audio_index = int(end_audio[s]/precision*sampling_frequency)
                    # zero the positions we do not want
                    audio_mask[beg_audio_index:end_audio_index] = 0
                filtered_data = data[audio_mask.astype(bool)]
                if first:
                    out = np.copy(filtered_data)
                    first = False
                    min_length = filtered_data.shape[0]
                else:
                    if filtered_data.shape[0] < min_length:
                        min_length = filtered_data.shape[0]
                    out = out[:min_length]
                    out += filtered_data[:min_length]
            wavfile.write(os.path.join(out_wav_dir, p+'.wav'),
                          int(sampling_frequency), out)


if __name__ == "__main__":
    # execute only if run as a script
    main()
