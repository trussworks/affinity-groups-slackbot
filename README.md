# affinity groups slackbot

We made this slackbot to allow folks to apply for admission into private affinity groups within a Slack workspace without forcing a public point of contact for the group to out themselves.


## dev environment

To work with the slackbot & test locally, you'll need:

- Python 3.6 or higher
  - Poetry
- Some environment variables as described in installation below
- Some linting is performed by pre-commit, so don't forget to `pre-commit install`


### working with the code

Install dependencies with command `poetry install` and keep them up-to-date with `poetry lock`.

To spin up the code locally, build the docker image via `docker build -t affinity:latest .` and `docker run -p 9000:8080 affinity:latest`


### running the tests

You can run the tests from project root with command `poetry run pytest`.


### deploying code to production

For Truss's instance of this bot, we have configured this to happen automatically on new commits to the `main` branch.
GitHub Actions will build and push the docker image to an ECR repository in the `trussworks-prod` AWS account.
In order to redeploy the lambda with the new image. You must copy and replace the image URI into the Terraform located in `trussworks-prod/affinity-groups-slackbot/main.tf` then apply.

```
module "lambda_affinity_groups" {
  source = "terraform-aws-modules/lambda/aws"

    ...

  image_uri    = REPLACE WITH COPIED IMAGE URI

  ...
}
```
