# How It Could Work

This is a sketch, not a spec. The protocol pieces would become an Application-category BSIP in `bitsocialnet/BSIPs` once the open questions are settled.

## Layers

| Layer | What it is | Built from |
|---|---|---|
| Revision | One version of one article, signed by its author | IPFS file addressed by CID, signed like a Bitsocial comment ([BSIP-2](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-2.md)) |
| Editorial group | A set of people, or an AI writer with human review, who decide which revision of each title is current in their version | A Bitsocial community ([BSIP-3](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-3.md)) |
| Group index | The group's signed map from article title to current revision CID | A signed, CID-addressed record like a community list ([BSIP-15](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-15.md)), sharded |
| Baseline | Every Wikipedia article, imported from the public dump | A group index published by whoever runs the import |
| Edit proposal | A revision someone asks a group to accept | A publication gated by the group's challenges ([BSIP-4](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-4.md)) |
| Client | Reads a title across the groups a reader follows and shows versions, diffs and history | A Bitsocial client |
| Search | Finds titles and full text | Competing indexers, or prebuilt search shards on IPFS |

## Revisions

A revision is an immutable file: the title, the article body, the CID of the revision it was based on, and the author's signature. Because it is content-addressed, anyone can host it and anyone can check it has not been altered. Because it names its parent, any chain of revisions is a verifiable history.

Revisions never change. Editing an article means publishing a new revision whose parent is the old one.

## Editorial Groups

A group is a Bitsocial community. Its owner and moderators decide which revision of each title is current in the group's version. The group publishes that decision as a signed index, and its community record points at the latest index. The group can have a `.bso` name like any community.

Groups can be anything:

- a few domain experts maintaining medicine or law articles,
- a political or national perspective that disagrees with Wikipedia on specific topics,
- an AI writer that regenerates articles from sources, with humans reviewing changes,
- a group that copies the baseline and only fixes vandalism.

A group's rules, sourcing standards and use of AI are its own. Readers decide which groups to follow.

### Why not one community per article

A Bitsocial community needs a node that stays online to receive publications over pubsub and keep republishing its IPNS record ([BSIP-3](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-3.md)). English Wikipedia alone has more than 7 million articles. One community per article would mean millions of always-online keys, which only one large operator could run. Editing comments also does not fit: a comment edit can only come from the comment's author ([BSIP-7](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-7.md)), so other people's changes could only arrive as replies.

With groups as communities, the number of communities grows with the number of editor groups, which is small.

## The Baseline and Overlays

The baseline is a group index covering every article in the Wikipedia dump. Wikipedia's text is CC BY-SA 4.0, so importing it is allowed with attribution and the same license.

A group index does not have to list every title. It lists only the articles the group has changed, and the client falls back to the baseline for the rest. So:

- a new group can exist with ten articles,
- storage and publishing cost grows with what a group changes, not with the size of the encyclopedia,
- every article exists from the first day.

The baseline has to be refreshed from new dumps on a schedule, by a job anyone can run and verify. The IPFS Wikipedia mirror went stale because nobody kept updating it: its English snapshot was from March 2021 when the repository was archived in July 2026.

Grokipedia content is not imported. It is under the xAI Community License, which can be revoked and requires xAI's notices on every copy, and there is no official dump.

## Edit Proposals

Anyone can propose a revision to a group. The proposal is published to the group over pubsub and passes the group's anti-spam challenges, like any Bitsocial publication. The group's moderators accept it, which updates the group index, or reject it.

A rejected proposal is still a signed revision. Another group can adopt it, or its author can start a group around it. That is the fork path: disagreement produces a new version instead of an edit war.

## The Client

For each title, the client:

1. resolves the revision in each group the reader follows, falling back to the baseline,
2. shows the reader's default group's version,
3. lists the other versions, grouped where they are identical,
4. shows diffs between any two versions and the signed history of each.

Readers choose their default groups. Clients can ship curated default lists, the way Bitsocial clients ship default community lists.

## Search

Full-text search over millions of articles cannot run on a phone without help. Two options, not exclusive:

- **Indexers.** Competing indexers crawl group indexes and serve search, as `bitsocial-indexer` does for communities. Any indexer can be replaced.
- **Prebuilt search shards.** A search index split into pieces and published on IPFS with the baseline, so clients fetch only the shards a query needs. Kiwix's ZIM files already bundle a full-text index with Wikipedia.

## Hosting and Takedowns

- Revisions and indexes stay available as long as someone keeps a copy: the group, readers who pin, or anyone who wants to.
- Each group needs a node online to accept proposals and publish its index. If a group's node disappears, its last published index and revisions still exist, and another group can copy them.
- Browser and mobile users reach the network through public RPCs and gateways. Those can be blocked or receive takedown notices. There is no single kill switch, but day-to-day access depends on having many of them.
- No one can remove a revision from the whole network. That includes defamation, doxxing and illegal material. Moderation happens in groups, clients and gateways, not in the protocol.

## Bitsocial Chain

Articles and indexes stay on IPFS. Bitsocial Chain would carry only the small facts that need global agreement or scarcity:

| Use | Why it needs a chain |
|---|---|
| `.bso` names for groups | A name must point to one group for everyone |
| Holder-gated voting on groups ([BSIP-18](https://github.com/bitsocialnet/BSIPs/blob/master/BSIPS/bsip-18.md)) | Token holdings are hard to fake, unlike accounts |
| Tips and bounties for editors | Payments need a shared ledger |
| Anchoring index CIDs (optional) | A recorded CID and time stop a group from showing different readers different versions or backdating its history |

None of these is needed to read or edit. Without them, groups are still addressed by public key, still publish indexes, and readers still choose.

## What Would Need a Spec

- The revision record format.
- The sharded group index and how the community record points to it.
- The edit proposal publication.
- How clients resolve a title across groups and the baseline.

These would go into one Application-category BSIP.
