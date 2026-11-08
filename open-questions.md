# Open Questions

Design decisions not yet made. These need answers before Infinipedia moves from idea to spec.

## Who Edits First

The hardest question is not technical. Earlier plural encyclopedias failed because editors stayed on Wikipedia.

- Who are the first three editorial groups, and why would they edit here instead of on Wikipedia?
- Which topics have people who already want their own version and cannot have it on Wikipedia?
- Can an AI-run group produce a version good enough that people read it, with a few humans reviewing?

## Choosing Between Versions

- How does a reader pick default groups without votes that fake accounts can inflate?
- Should clients ship curated default group lists, like default community lists? Who curates them?
- Could holder-gated pubsub voting ([BSIP-18](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-18.md)) or directories ([BSIP-19](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-19.md)) rank groups per topic?
- How should the client show agreement, for example "5 of the 7 groups you follow have the same version"?

## Illegal and Harmful Content

- What moderation do clients apply by default: blocklists, hidden groups, warnings?
- How are articles about living people handled, where defamation risk is highest?
- What should public RPC and gateway operators be able to refuse to serve, and how is that shown to readers?

## Article Format

- Wikitext matches the dump but depends on thousands of templates. HTML is easy to render but hard to edit and diff. Markdown is easy to edit but loses tables, infoboxes and references.
- How are links between articles resolved when a title differs between groups?
- Text only at first? Images on Wikimedia Commons each carry their own license.

## Scale

- How big is a sharded index for a group with a few hundred changed articles, and for the baseline with millions?
- How often can a group publish a new index, and what does each update cost?
- What is the largest publication pkc-js accepts over pubsub, and do long articles fit in one revision?

## The Baseline

- Who runs the import, how often, and how do others verify it matches the official dump?
- When the baseline changes an article a group has overlaid, how does the group see that and decide whether to merge?

## AI-Run Groups

- Should a group have to declare that it uses AI, and which model?
- Should AI-written revisions be marked differently from human ones?

## Bitsocial Chain

- Should groups anchor their index CIDs on the chain, how often, and who pays for it?
- Should clients warn when a group's index doesn't match its latest anchor?
- Who funds editor bounties, and who decides when a bounty is earned?

## Licensing

- Content imported from Wikipedia must stay CC BY-SA 4.0. Should original articles be required to use the same license so versions can always be merged?
- How is attribution to Wikipedia shown in the client?

## Search

- Indexers, prebuilt shards on IPFS, or both?
- Can a phone search the baseline offline with downloaded shards?
