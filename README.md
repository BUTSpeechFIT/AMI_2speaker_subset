# AMI_2speaker_subset

Recipe to create 2-speaker "conversations" from the AMI corpus[1]. The reference annotations and partition are taken from https://github.com/BUTSpeechFIT/AMI-diarization-setup

The recipe will create all possible combinations of two speakers for each recording by removing speech from other speakers. Audio where a speaker of interest overlaps with a speaker to be removed is also removed.



[1] J. Carletta, S. Ashby, S. Bourban, M. Flynn, M. Guillemot, T. Hain, J. Kadlec, V. Karaiskos, W. Kraaij, M. Kronenthal, et al., The AMI meeting corpus: A pre-announcement, in: International workshop on machine learning for multimodal interaction, Springer, 2006, pp. 28–39.


### Citations
In case of using the setup, please cite:\
Federico Landini, Mireia Diez, Alicia Lozano-Diez, Lukáš Burget: [Multi-Speaker and Wide-Band Simulated Conversations as Training Data for End-to-End Neural Diarization](https://arxiv.org/abs/2211.06750)
```
@article{landini2022multispeaker,
  title={Multi-Speaker and Wide-Band Simulated Conversations as Training Data for End-to-End Neural Diarization},
  author={Landini, Federico and Diez, Mireia and Lozano-Diez, Alicia and Burget, Luk{\'a}{\v{s}}},
  journal={arXiv preprint arXiv:2211.06750},
  year={2022}
}
```

## Contact
If you have any comment or question, please contact landini@fit.vutbr.cz
