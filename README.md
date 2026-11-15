<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="design/logo/infinipedia-mark-on-dark.png" />
  <img src="design/logo/infinipedia-mark-on-light.png" alt="Infinipedia logo" width="120" />
</picture>

# Infinipedia

An idea for an encyclopedia on Bitsocial that nobody owns.

[How it could work](how-it-could-work.md) · [Open questions](open-questions.md) · [Logo](design/logo/README.md)

</div>

Editorial groups each maintain their own version of the encyclopedia, and readers choose whose versions they trust. No foundation, company or AI model decides what the encyclopedia says.

- **Plural versions.** Each group publishes its own version of the articles it edits, over a shared Wikipedia baseline.
- **Signed revisions.** Every revision is signed by its author and names its parent, so history is verifiable.
- **Forkable.** Anyone can fork any version and start a group of their own.
- **The reader decides.** On a contested article, the reader sees which versions disagree and where.

> [!NOTE]
> **Idea stage.** This repository reserves the name and collects the design. Nothing here is built. It fits [Phase 5 of the Bitsocial master plan](https://bitsocial.net/#master-plan-phase-5), the long tail of Bitsocial clients, and depends on earlier phases: public RPCs, `.bso` names, an indexer and, for voting and payments, Bitsocial Chain.

## The thesis

Wikipedia's text is already impossible to delete. It is licensed CC BY-SA 4.0, published as public dumps, copied offline by Kiwix and has been mirrored on IPFS. What is centralized is the editorial process: one community of editors and admins settles contested articles, decides which sources count as reliable and publishes one version of each title.

Grokipedia centralizes that process further. Its articles are written by one company's AI model, and its content is licensed under the xAI Community License, which xAI can revoke.

Neither problem is solved by hosting the same single version somewhere harder to take down. Infinipedia makes the version plural instead:

| | Wikipedia | Grokipedia | Infinipedia |
| --- | --- | --- | --- |
| Who writes | Volunteer editors | Grok, xAI's model | Competing editorial groups: human, AI-assisted or AI-run |
| Who settles contested articles | Wikipedia's editors and admins | xAI | Each group for its own version; the reader picks between groups |
| Versions per article | One | One | One per group that edits it, plus the baseline |
| Content license | CC BY-SA 4.0 | xAI Community License; some pages CC BY-SA 4.0 | CC BY-SA 4.0, inherited from the Wikipedia baseline |
| Hosting | Wikimedia Foundation servers | xAI servers | IPFS and each group's own node |
| Can one party stop editing | Yes | Yes | No |

The goal is not an unbiased encyclopedia. Every editor has views. The goal is that biases are plural and visible: on a contested article, the reader sees that versions disagree, sees exactly where, and decides whom to trust.

## Compare versions

The feature neither Wikipedia nor Grokipedia can offer is the comparison view. For any article, the client shows:

- The version from the reader's default group.
- How many other groups have their own version, and which ones.
- A diff between any two versions, including the Wikipedia baseline.
- Each version's signed history: who changed what, and which group accepted it.

Uncontested articles, which are most of them, look like an ordinary encyclopedia. Contested ones show the disagreement instead of hiding it behind one group's decision.

## Why now

Earlier attempts at a plural or decentralized encyclopedia, such as Citizendium and Larry Sanger's [Encyclosphere](https://encyclosphere.org/), ran into the same wall: maintaining millions of articles takes thousands of editors, and the editors stayed on Wikipedia.

AI changes that cost. Grokipedia showed that one company with a model can produce millions of articles within months. A small editorial group with an AI writer can now maintain a full version of the encyclopedia and spend its human effort on the articles it actually disagrees about. Infinipedia also does not ask groups to rewrite everything: every group starts from the Wikipedia baseline and only publishes the articles it changes. See [how-it-could-work.md](how-it-could-work.md#the-baseline-and-overlays).

## What it is not

- **Not a mirror.** Mirroring Wikipedia on IPFS was done years ago. It shows that hosting is easy and that a mirror nobody updates goes stale.
- **Not one community per article.** Every Bitsocial community needs an always-online node. Millions of articles would mean millions of always-online keys, which in practice means one operator. Communities are editorial groups, so their number grows with editors, not articles.
- **Not a Grokipedia mirror.** Grokipedia content is not imported. Its license is revocable and there is no official dump.

## Why IPFS, not a blockchain

A blockchain exists to make everyone agree on one shared state. Infinipedia is designed so nobody has to agree: each group decides its own version and readers choose. Putting articles on a chain would bring back one official version decided by validators or token holders, charge a fee for every edit, and make every node store millions of articles.

The content doesn't need a chain:

- Revisions are content-addressed and signed, so tampering is detectable.
- Each revision names its parent, so history is verifiable.
- Each group's index sits behind its community's key, so only the group can update it.
- Anyone can host any of it.

[Bitsocial Chain](https://chain.bitsocial.net) fits the parts that need global agreement or scarcity:

- `.bso` names for groups.
- Holder-gated voting to rank groups without votes from fake accounts.
- Tips and bounties for editors.
- Optionally, anchoring each group's index CID on the chain, so a group can't show different readers different versions or backdate its history.

Articles live on IPFS; only small global facts go on the chain. That is the same split Bitsocial uses for social media.

## Documents

| Document | Contents |
| --- | --- |
| [how-it-could-work.md](how-it-could-work.md) | Revisions, editorial groups, the baseline, edit proposals, the client, search, hosting and Bitsocial Chain |
| [open-questions.md](open-questions.md) | Design decisions not yet made |
| [design/logo](design/logo/README.md) | The logo, its files and how it is built |

## Ecosystem

| Project | Role |
| --- | --- |
| [Bitsocial](https://bitsocial.net) | Protocol docs |
| [BSIPs](https://github.com/bitsocialnet/BSIPs) | Bitsocial Improvement Proposals |
| [bitsocial-indexer](https://github.com/bitsocialnet/bitsocial-indexer) | Indexer |
| [Bitsocial Chain](https://chain.bitsocial.net) ([repo](https://github.com/bitsocialnet/bitsocial-chain)) | Names, voting and payments |
| [WeTube](https://github.com/bitsocialnet/wetube) | Sibling idea-stage repo: YouTube alternative |
| [GitCommons](https://github.com/bitsocialnet/gitcommons) | Sibling idea-stage repo: GitHub alternative |

## License

[GPL-3.0-or-later](LICENSE) for this repository. Encyclopedia content would be CC BY-SA 4.0; see [open-questions.md](open-questions.md#licensing).
