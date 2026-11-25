const {test} = require("node:test");
const assert = require("node:assert/strict");
const prepareRelease = require("../prepare_release.cjs");

for (const immutable of [true, false]) {
  test(`preserves published release (immutable=${immutable})`, async () => {
    const outputs = {};
    await execute([{tag_name: "v1", draft: false, immutable, html_url: "release-url"}], outputs);
    assert.equal(outputs.publish, "false");
  });
}

test("allows a new release, ignoring other tags", async () => {
  const outputs = {};
  await execute([{tag_name: "other", draft: true}], outputs);
  assert.equal(outputs.publish, "true");
});

test("rejects existing drafts without claiming publication succeeded", async () => {
  const outputs = {};
  await assert.rejects(execute([{tag_name: "v1", draft: true}], outputs), /already has a draft/);
  assert.deepEqual(outputs, {});
});

test("propagates API permission failures", async () => {
  await assert.rejects(
    prepareRelease({
      github: {rest: {repos: {listReleases: "list"}}, paginate: async () => {throw new Error("Forbidden");}},
      context: {repo: {}}, core: {}, tag: "v1",
    }),
    /Forbidden/
  );
});

async function execute(releases, outputs) {
  return prepareRelease({
    github: {
      rest: {repos: {listReleases: "list"}},
      paginate: async (method, options) => {
        assert.equal(method, "list");
        assert.deepEqual(options, {owner: "owner", repo: "repo", per_page: 100});
        return releases;
      },
    },
    context: {repo: {owner: "owner", repo: "repo"}},
    core: {info: () => {}, setOutput: (key, value) => {outputs[key] = value;}},
    tag: "v1",
  });
}
