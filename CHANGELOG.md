# CHANGELOG

<!-- version list -->

## v1.3.0 (2025-06-19)

### Chores

- Update FastAPI version to 1.2.1 in main application file
  ([`4fac1af`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/4fac1af28e9dd9f40b79f2e4f81735595cbc9fa1))

### Continuous Integration

- Add task definition download step in GitHub Actions workflow for ECS deployment
  ([`8195167`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/8195167961a2f51afb43c48129529a4baf262956))

- Enhance GitHub Actions workflow to retrieve semantic version and build ECR image URL dynamically
  ([`92420fb`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/92420fb1c26e7524a4d8b0634ea0d33454493697))

- Refactor GitHub Actions workflows for improved readability and consistency in formatting and
  indentation
  ([`c2e7314`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/c2e73146046ef7a8647fca3026ff7d4bc324583c))

- Set fetch-depth to 0 in GitHub Actions workflows for full history checkout
  ([`40acb83`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/40acb83aa8dc548733babd2636afa543c4c57e9d))

- Update deployment conditions in GitHub Actions to trigger on successful main branch workflow runs
  ([`deead8c`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/deead8c562f7dd4c74ebe5b1bbae1a8286f73bb0))

- Update Python version to 3.12 and upgrade python-semantic-release to 10.1.0 in GitHub Actions
  workflows
  ([`8ff885a`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/8ff885a3b05eafac60b9be2d36c553f12ba09a6e))

### Features

- Update FastAPI application title and modify wellness profile route tag for clarity
  ([`a2a92f4`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/a2a92f4a0b82370006dc3c727d76a1a98ca4dd82))


## v1.2.1 (2025-06-19)

### Bug Fixes

- Correct branch pattern in deployment workflow from 'releases/**' to 'release/**'
  ([`c4bbc15`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/c4bbc153453a31f441f8bc054c7e5e08cb4e14ba))


## v1.2.0 (2025-06-19)

### Features

- Add new deployment workflows for development and production environments in GitHub Actions
  ([`388c4b3`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/388c4b39aaa13fb1d090f8cf32a1860cfefd0c72))


## v1.1.0 (2025-06-19)

### Chores

- Enhance GitHub Actions workflow to configure AWS credentials and automate Docker image build and
  push to ECR
  ([`3c8e607`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/3c8e60742cc4015b78275e8520691c45f7e5cf45))

- Optimize GitHub Actions workflow for Docker image build and push to ECR using BuildKit and
  improved caching
  ([`75861e3`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/75861e3fa9d0136e3451daf647df2fee3172ca26))

- Refactor GitHub Actions workflow to use consistent variable syntax for AWS ECR repository URL in
  Docker build and push steps
  ([`76a8386`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/76a83863991c789e07a58ce1aa84bfff9adbe74f))

- Update GitHub Actions workflow to export AWS account ID and repository URL for Docker image build
  and push to ECR
  ([`523ef8c`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/523ef8c039000eb6c5b2f0c52dccf90b37028833))

- Update GitHub Actions workflow to grant write permissions for id-token
  ([`5a8d6f3`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/5a8d6f3816ec47596559e21b9657a0ca50a82d94))

### Continuous Integration

- Consolidate GitHub Actions workflows into a single 'Formatting, Linting and Testing' workflow,
  replacing the previous linting workflow and integrating security checks with Snyk, SonarQube, and
  Gitleaks
  ([`1831b10`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/1831b1089508092ed5e872ee45a6d9edaf87f2e3))

- Enhance GitHub Actions workflows by adding concurrency control, caching for dependencies, and
  improved error handling for SonarQube and Gitleaks steps
  ([`d2b00f4`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/d2b00f4f7f1df4a58248bcbc8aa1a6160222c328))

- Simplify GitHub Actions workflow by consolidating Ruff linting and formatting steps into single
  run commands
  ([`c759b1d`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/c759b1d544024c896a7bff5545a47ebe35b24e29))

- Update GitHub Actions workflow to remove dependency installation step and pin Snyk action to
  master branch for improved flexibility
  ([`2838247`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/2838247e8f68a3450f1b45ec7ec0fdafbeeb3e2c))

### Features

- Update GitHub Actions workflow to add image digest output and implement deployment to development
  environment
  ([`84368fb`](https://github.com/the-training-arc/fastapi-llm-ws-demo/commit/84368fb24ab4417f3e209c85402a7ca128564761))


## v1.0.0 (2025-06-16)

- Initial Release
