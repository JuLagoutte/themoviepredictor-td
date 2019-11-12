class Movie:
    def __init__(self,
                imdb_id, 
                title, 
                original_title, 
                genre, 
                synopsis, 
                tagline, 
                duration, 
                production_budget, 
                marketing_budget, 
                release_date, 
                rating, 
                imdb_score, 
                box_office,
                popularity,
                awards,
                is_3D):
        
        self.id = None
        self.title = title
        self.original_title = original_title
        self.duration = duration
        self.release_date = release_date
        self.rating = rating
        self.box_office = box_office
        self.imdb_id = imdb_id
        self.imdb_score = imdb_score
        self.synopsis = synopsis
        self.tagline = tagline
        self.popularity = popularity
        self.awards = awards
        self.genre = genre

        self.is_3D = None
        self.production_budget = production_budget
        self.marketing_budget = None

        self.actors = []  # création liste vide car on sait qu'il y a des acteurs dans le film mais on ne connaît pas encore lesquels
        self.productors = []


    def total_budget(self):
        if (self.production_budget == None or self.marketing_budget == None):
            return None
        return self.production_budget + self.marketing_budget

 