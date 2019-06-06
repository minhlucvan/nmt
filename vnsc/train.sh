 ./.venv/bin/python  -m nmt.nmt \
    --src=ko --tgt=co \
    --hparams_path=nmt/standard_hparams/iwslt15.json \
    --out_dir=vnsc/model \
    --vocab_prefix=vnsc/data/vocab \
    --train_prefix=vnsc/data/train \
    --dev_prefix=vnsc/data/dev \
    --check_special_token=false \
    --test_prefix=vnsc/data/test
