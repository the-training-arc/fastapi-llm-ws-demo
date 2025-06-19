# CHANGELOG

<!-- version list -->

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
