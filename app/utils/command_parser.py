def parse_command(action):
    """ Parses the interpreted command to extract action details and parameters. """
    action_details = {}
    if "deploy" in action:
        # Example action: "deploy with id 123 on branch master"
        words = action.split(" ")
        try:
            action_details["type"] = "deploy"
            action_details["pipeline_id"] = words[words.index('id') + 1]
            action_details["branch"] = words[words.index('branch') + 1]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for deployment action")
    elif "backup" in action:
        # Example action: "backup to storage_account_name container_name"
        words = action.split(" ")
        try:
            action_details["type"] = "backup"
            action_details["storage_account_name"] = words[words.index('to') + 1]
            action_details["container_name"] = words[words.index('container_name') + 2]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for backup action")
    elif "restore" in action:
        words = action.split(" ")
        try:
            action_details["type"] = "restore"
            action_details["storage_account_name"] = words[words.index('from') + 1]
            action_details["container_name"] = words[words.index('container_name') + 2]
            action_details["blob_name"] = words[words.index('blob_name') + 2]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for restore action")
    elif "metrics" in action:
        words = action.split(" ")
        try:
            action_details["type"] = "metrics"
            action_details["subscription_id"] = words[words.index('for') + 1]
            action_details["resource_group_name"] = words[words.index('group') + 1]
            action_details["storage_account_name"] = words[words.index('account') + 2]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for metrics action")
    elif "deploy-terraform" in action:
        words = action.split(" ")
        try:
            action_details["type"] = "deploy-terraform"
            action_details["environment"] = words[words.index('environment') + 1]
            action_details["region"] = words[words.index('region') + 1]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for deploy-terraform action")
    elif "apply-terraform-plan" in action:
        words = action.split(" ")
        try:
            action_details["type"] = "apply-terraform-plan"
            action_details["provision_path"] = words[words.index('path') + 1]
        except (ValueError, IndexError) as e:
            raise ValueError("Missing required parameters for apply-terraform-plan action")
        
        