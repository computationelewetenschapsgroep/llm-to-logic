# llm-to-logic
Rebasing and squashing are not allowed as rewriting commits introduces additional efforts to merge and solve conflicts.

Below the steps to run in the Git workflow.
1. Create a local dev branch from master:
```bash
git checkout -b [name_of_your_new_branch]
```
2. Create the remote dev branch:
```bash
git push --set-upstream origin [name_of_your_new_branch]
```
3. Start adding the files you modified:
```bash
git add files_you_modified
```
4. Commit your changes:
```bash
git commit -m "Your descriptive commit message."
```
5. When required, merge changes from another remote branch with:
```bash
git fetch
git merge origin/[name_of_the_other_branch]
```
5. Push your changes to the remote dev branch:
```bash
git push
```
6. Open the merge request by visiting the URL given in the result of the push command.
7. To merge a request, make sure it has been reviewed and approved. Note that the checkbox 'Squash commits' should remain disabled otherwise the Gitlab CI will break.
