# 5090 non-Llama paper-version assets are on D, claims not run

2026-11-05. No new PODR integer and no new W1-OD id. The download order was to fetch every experiment asset except Llama 2 7B chat, at the frozen paper/artifact revisions, and to stop before a claim run.

Llama 2 7B chat was not downloaded. Claim 1, 2 and 3 remain NOT_RUN. ASR and accuracy remain NOT_MEASURED. No model was loaded. `trust_remote_code` was not used. No paid API. No D1/D2/D3. Upstream source was not edited. Upstream HEAD remains `ba2a17efba165d45409114df2d70b030ade1e1b8`.

The earlier return still said the BEIR unpack cap was not frozen. Before the first zip byte was extracted, this run enforced the already proposed stop: abort if the zip central-directory size exceeds 8 times the official Content-Length, if a path escapes the destination, or if D would fall below 20 GiB. All three archives stayed under that cap. The extracted sizes below are measurements from that central directory and they match the files on disk.

## Models

Cache is the D-drive Hub cache `upstream/hf_cache`. No token was sent. Official revisions only.

| Asset | Revision | Files | Bytes on disk | Cap used |
| --- | --- | --- | --- | --- |
| `lmsys/vicuna-7b-v1.3` | `236eeeab96f0dc2e463f2bebb7bb49809279c6d6` | 8 weight/tokenizer files | 13477478468 | 26954326092 |
| `facebook/contriever` | `2bd46a25019aeea091fd42d1f0fd4801675cf699` | 6 | 438706178 | 875963049 |
| `sentence-transformers/paraphrase-MiniLM-L6-v2` | `c9a2bfebc254878aee8c3aca9e6844d5bbb102d1` | 10, including `1_Pooling/config.json` and `model.safetensors` | 91567611 | 1111304665 |

Not downloaded: Llama 2, DPR, ANCE, 13B, `all-MiniLM-L6-v2`, MiniLM ONNX, OpenVINO, TensorFlow, and the MiniLM PyTorch duplicate. Vicuna's connection dropped eight times with `ChunkedEncodingError`; the same revision resumed and finished. The byte gaps versus the earlier tree sums are the unread README and `.gitattributes` files.

## BEIR

Official Darmstadt zips. Downloaded lengths match the earlier HEAD values and ETags.

| Set | Zip bytes | ETag | Extracted bytes | Cap |
| --- | --- | --- | --- | --- |
| nq | 498307926 | `6075b282-1db39356` | 1504181461 | 3986463408 |
| hotpotqa | 654025350 | `60019b87-26fba286` | 2183814339 | 5232202800 |
| msmarco | 1082258632 | `6074501d-4081f4c8` | 3618904334 | 8658069056 |

Extracted layout is `artifacts/datasets/{nq,hotpotqa,msmarco}` with `corpus.jsonl`, `queries.jsonl` and `qrels/`. NQ has `qrels/test.tsv`. HotpotQA and MS MARCO have train, dev and test qrels. The corpora are not in git. D free space after the download was 769336549376 bytes.

## Still required before a claim

A later run has to set `HF_HOME` and `HUGGINGFACE_HUB_CACHE` to the D cache above, or the loader will not see these snapshots. It also has to stay offline after that. Llama 7B cells cannot run. Claim 2 still has the unpatched log-directory mismatch. This download does not approve Claim 1, 2 or 3.

Raw log sha256 `4833e2b7204434c4fbc20131b2b0b49f0c9c0d76a446f6577076435bb3b4f051`. Status sha256 `274142eed7e3819b40a26dc8a5ad167ccecd49e7d5d7852f525c97143785c829`. Both stay outside the research git.
