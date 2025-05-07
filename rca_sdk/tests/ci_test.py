from rca_sdk.plugins.ci import github_actions

config = {
    "token": "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",
    "repo": "https://github.com/anon-cypher/RCA_SDK_TEST/tree/main"
}

print(github_actions.get_recent_workflow("auth-service", config))
