# Continue the latest House World work from R6

The latest Codex/Claude integration and responsive follow-up are on **PR #46**, branch **`corr/review-dt-design-r6`** in `ojfbot/lego-village-pipeline`.

Read the [structured Claude Design pickup guide](https://github.com/ojfbot/lego-village-pipeline/blob/e32add01a96f5a24e8ef3aabc3087a3d5bf60004/CLAUDE-DESIGN-PICKUP.md) or its [raw Markdown](https://raw.githubusercontent.com/ojfbot/lego-village-pipeline/e32add01a96f5a24e8ef3aabc3087a3d5bf60004/CLAUDE-DESIGN-PICKUP.md). If your GitHub connector reads branches by name, explicitly select `corr/review-dt-design-r6`.

The working prototype is `docs/design/review/DT-DESIGN-R6-addendum/prototype/`, pinned at `4bf12c8370d341a2bd8d1094491e281ebd6637ec`. It combines the R6 interface with the GPT-quality renderer, corrected model pair, responsive sheets/dashboard and navigation fixes. Both Blender revisions and verification are included.

Read `review.md` and `follow-up-tasks.json` in the addendum folder. The [posted follow-up review](https://github.com/ojfbot/lego-village-pipeline/pull/46#pullrequestreview-5498479017) assigns dedicated Grid/Subgrid, navigation and motion/transformation work. These files provide the same task content for a connector that cannot read PR reviews.

This PR #45 branch contains the earlier HOUSE-WORLD R0 and bottom-step export correction. Those remain useful source history. The later R6 files live on the separate PR #46 branch. Searching only this branch or `main` cannot establish their absence.

For upload-based pickup, James has a `claude-design-r6-pickup.zip` containing the tracked R6 repository source and a prebuilt `browser-preview/`. The R6 pickup guide describes how to use it. The local Mac URL at port 4200 is a preview, not a remote transfer endpoint.

The frozen original packages on this branch stay unchanged. This pointer adds discoverability only.
