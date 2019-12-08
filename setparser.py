import argparse

class Parser :

    def set_parser(self):

        parser = argparse.ArgumentParser(description='Process MoviePredictor data')

        parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')

        action_subparser = parser.add_subparsers(title='action', dest='action')

        list_parser = action_subparser.add_parser('list', help='Liste les entitÃ©es du contexte')
        list_parser.add_argument('--export' , help='Chemin du fichier exportÃ©')

        find_parser = action_subparser.add_parser('find', help='Trouve une entitÃ© selon un paramÃ¨tre')
        find_parser.add_argument('id' , help='Identifant Ã  rechercher')

        insert_parser = action_subparser.add_parser('insert', help='insérer une donnée dans la database')

        import_parser = action_subparser.add_parser('import', help='Importer de nouvelles données')
        import_parser.add_argument('--file', help='nom du fichier à recuperer')
        import_parser.add_argument('--api', help='nom de API utilisée')
        import_parser.add_argument('--year', help='année des films recherchés')
        import_parser.add_argument('--imdb_id', help='Id du film recherché sur API')

        know_args = parser.parse_known_args()[0]

        # if know_args.api: #== 'omdb':
        #     year_parser = import_parser.add_argument('--year', help='année des films recherchés')
        #     imdbId_parser = import_parser.add_argument('--imdb_id', help='Id du film recherché sur API')

        # if know_args.api == 'themoviedb':
        #     year_parser = import_parser.add_argument('--year', help='année des films recherchés')
        #     imdbId_parser = import_parser.add_argument('--imdb_id', help='Id du film recherché sur API')

        # if know_args.api == 'all_api':
        #     year_parser = import_parser.add_argument('--year', help='année des films recherchés')
        #     imdbId_parser = import_parser.add_argument('--imdb_id', help='Id du film recherché sur les API')

        if know_args.context == "people":
            insert_parser.add_argument('--firstname', help='prenom', required=True)
            insert_parser.add_argument('--lastname', help='nom de famille', required=True)

        if know_args.context == "movies":
            insert_parser.add_argument('--title', help='le titre en france', required=True)
            insert_parser.add_argument('--original_title', help='titre original', required=True)
            insert_parser.add_argument('--synopsis', help='le synopsis du film')
            insert_parser.add_argument('--duration', help='la durée en minute du film', required=True)
            insert_parser.add_argument('--rating', help='la classification pour visionnage du public', choices=('TP', '-12', '-16', '-18'), required=True)
            insert_parser.add_argument('--production_budget', help='le budget du film')
            insert_parser.add_argument('--marketing_budget', help='le budget pour la promo du film')
            insert_parser.add_argument('--release_date', help='la date de sortie', required=True)  
        
        args = parser.parse_args()
        return args