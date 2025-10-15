import data_jobs
from models.season import Season

def main():
    print("Starting...")

    # Specify the seasons to run here
    years = [2024]

    # Build our configs, which also caluclate all of the season coefficients (e.g. for wOBA)
    seasons = []
    for year in years:
        s = Season(year)

        s.print_data('batter')

        seasons.append(s)

    # Run the data_jobs, passing that config object

    # data_jobs.run()

if __name__ == '__main__':
    main()