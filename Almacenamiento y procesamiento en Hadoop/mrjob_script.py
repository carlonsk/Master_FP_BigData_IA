from mrjob.job import MRJob

class MRPointsAway(MRJob):

    def mapper(self, _, line):
        data = line.split(',')
        away_team = data[2]
        ftr = data[6] 
        if ftr == 'A':
            points = 3
        elif ftr == 'D':
            points = 1
        else:
            points = 0
        yield away_team, points

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRPointsAway.run()
# TODO: muestra la salida de la ejecución del proceso MapReduce en local o en Hadoop.
