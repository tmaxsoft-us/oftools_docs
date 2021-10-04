# Contributing to OpenFrame Tools Documentation <!-- omit in toc -->

🎉 First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to oftools_docs, which is hosted on GitHub, in the TmaxSoft Organization. These are mostly guidelines, not rules. Use your best judgment, and feel free to suggest changes to this document in a pull request.

## Table of Contents <!-- omit in toc -->

* [How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Direct Contribution](#direct-contribution)
* [Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Other project rules](#other-project-rules)

## How Can I Contribute?

### Reporting Bugs

Create a GitHub issue with the label **bug**. When you are creating a bug report, please include as many details as possible. The more details, the better it is to troubleshoot and solve the issue as fast as possible.

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened.

### Suggesting Enhancements

Create a GitHub issue with the labels **enhancement** and/or **documentation** with a detailed description of your idea of enhancement. The project development team will then study the idea, including feasibility and the time needed to implement it. You will be able to follow the state of progress, whether the idea has been validated or rejected, and much more information on this same issue.

Before submitting an enhancement suggestion, perform a search to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

### Direct Contribution

You can also directly participate to the documents of this repository. Clone the repository to your local machine, and create your own branch. Naming conventions are as follows:

  - it has to start with 'dev'
  - it has to be short, under 20 characters
  - it has to be a list of keywords relevant to what you are implementing
  - if there are multiple words, they have to be separated with a '-' character

Then, you can start working on your dedicated branch, applying changes to the documents and pushing your commits. When you are done working on it, you can open a pull request, assigning it to @ClementDeltel for review.

The idea remains the same if you choose to fork the project instead of cloning it. There is just no specific branch that you need to create.

## Styleguides

### Git Commit Messages

- Respect the following format:
```
📝RM#xxxx-x: ...

What: ...
Why: ...
```

- RM stands for Redmine. After, please specify the ticket number (xxxx) and the action number (-x).
- Explain **What** has been changed and **Why** you applied these changes.
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Consider starting the commit message with an applicable emoji:
  - 🎨: when improving the format/structure of the code
  - 🐎: when improving performance
  - 🚱: when plugging memory leaks
  - 📝: when writing docs
  - 🐧: when fixing something on Linux
  - 🐛: when fixing a bug
  - 🔥: when removing code or files
  - ✅: when adding tests
  - 🔒: when dealing with security
  - ⬆️: when upgrading dependencies
  - ⬇️: when downgrading dependencies

These are only a few examples, please find the full list of compatible emojis and their meaning [here](https://gitmoji.dev/).


### Other project rules 

- This is a documentation project, so please use a spell checking tool like [Grammarly](https://www.grammarly.com/) to avoid typographical and any other type of errors