./.venv/bin/python -m vnsc.scripts.vnsc

#  ./.venv/bin/subword-nmt learn-bpe -s 1 < ./vnsc/data/train.ko > ./vnsc/data/code.ko
# ./.venv/bin/subword-nmt apply-bpe -c ./vnsc/data/code.ko < ./vnsc/data/train.ko | ./.venv/bin/subword-nmt get-vocab > ./vnsc/data/vocab.ko
# ./.venv/bin/subword-nmt learn-bpe -s 1 < ./vnsc/data/train.co > ./vnsc/data/code.co
# ./.venv/bin/subword-nmt apply-bpe -c ./vnsc/data/code.co < ./vnsc/data/train.co | ./.venv/bin/subword-nmt get-vocab > ./vnsc/data/vocab.co

./.venv/bin/python vnsc/scripts/gen_vocab.py  ./vnsc/data/train.co  vnsc/data/vocab.co
./.venv/bin/python vnsc/scripts/gen_vocab.py  ./vnsc/data/train.ko  vnsc/data/vocab.ko
