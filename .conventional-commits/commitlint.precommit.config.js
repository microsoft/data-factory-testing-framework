module.exports = {
    extends: ['@commitlint/config-conventional'],
    defaultIgnores: false,
    ignores: [
        // allow fixup and squash commits for precommit checks
        (c) => new RegExp('(fixup|squash)!').test(c),
    ],
};
