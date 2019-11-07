class Movie:
    def __init__(self, omdb_id, title, original_title, duration, release_date, rating, imdb_score, box_office):
        self.id = None
        self.title = title
        self.original_title = original_title
        self.duration = duration
        self.release_date = release_date
        self.rating = rating
        self.box_office = box_office
        self.omdb_id = omdb_id
        self.imdb_score = imdb_score

        self.actors = []  # création liste vide car on sait qu'il y a des acteurs dans le film mais on ne connaît pas encore lesquels
        self.productors = []
        self.is_3D = None
        self.production_budget = None
        self.marketing_budget = None

    def total_budget(self):
        if (self.production_budget == None or self.marketing_budget == None):
            return None
        return self.production_budget + self.marketing_budget

 