class SubscriptionTier:
    TIER_DEFINITIONS = {
        'Free': {
            'feature_access': ['basic_feature'],
            'resource_limit': 1,
            'api_rate_limit': 100,
        },
        'Basic': {
            'feature_access': ['basic_feature', 'standard_feature'],
            'resource_limit': 5,
            'api_rate_limit': 500,
        },
        'Professional': {
            'feature_access': ['basic_feature', 'standard_feature', 'premium_feature'],
            'resource_limit': 10,
            'api_rate_limit': 1000,
        },
        'Enterprise': {
            'feature_access': ['basic_feature', 'standard_feature', 'premium_feature', 'enterprise_feature'],
            'resource_limit': 50,
            'api_rate_limit': 5000,
        },
        'Galactic': {
            'feature_access': ['all_features'],
            'resource_limit': 'unlimited',
            'api_rate_limit': 'unlimited',
        },
    }

    def __init__(self, user_tier):
        self.user_tier = user_tier
        self._validate_tier()

    def _validate_tier(self):
        if self.user_tier not in self.TIER_DEFINITIONS:
            raise ValueError(f"Invalid tier: {self.user_tier}")

    def get_features(self):
        return self.TIER_DEFINITIONS[self.user_tier]['feature_access']

    def get_resource_limit(self):
        return self.TIER_DEFINITIONS[self.user_tier]['resource_limit']

    def get_api_rate_limit(self):
        return self.TIER_DEFINITIONS[self.user_tier]['api_rate_limit']

    def update_tier(self, new_tier, consent_given):
        if not consent_given:
            raise PermissionError("Consent must be verified before tier change.")
        self.user_tier = new_tier

    def scale_resources(self):
        # Logic to scale resources dynamic based on user tier
        pass

    def feature_set_updates(self):
        # Logic to update features when tier changes
        pass
        
# Example usage:
# user_subscription = SubscriptionTier('Free')
# print(user_subscription.get_features())
