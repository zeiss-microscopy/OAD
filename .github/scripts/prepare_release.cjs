module.exports = async function prepareRelease({ github, context, core, tag }) {
  const releases = await github.paginate(github.rest.repos.listReleases, {
    ...context.repo,
    per_page: 100,
  });
  const matches = releases.filter(release => release.tag_name === tag);
  if (matches.some(release => release.draft)) {
    throw new Error(
      `Release "${tag}" already has a draft. No release or assets were changed. ` +
      "Inspect the previous publication error before proceeding. If GitHub reports " +
      "'tag_name was used by an immutable release', the tag cannot be reused; " +
      "select an unused release_suffix when publishing from master, or prepare a new package version."
    );
  }
  if (matches.length > 1) {
    throw new Error(`Multiple published releases found for "${tag}"; refusing to modify them.`);
  }
  if (matches.length === 1) {
    core.info(`Preserving published release "${tag}": ${matches[0].html_url}`);
    core.setOutput("publish", "false");
    return;
  }
  core.info(`No existing release for "${tag}"; publication may proceed.`);
  core.setOutput("publish", "true");
};
