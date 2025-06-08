class RankingGeneratorConfig:
    #TODO: move this to an actual config file
    def __init__(self, min_submissions = 3,
                       max_submissions = 24):
        self.min_submissions = min_submissions
        self.max_submissions = max_submissions
