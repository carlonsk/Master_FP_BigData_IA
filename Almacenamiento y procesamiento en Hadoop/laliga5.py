#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime

class LaLigaRecentPerformance(MRJob):

    SORT_VALUES = True

    def mapper_score(self, _, line):
        _, date, _, home_team, away_team, _, _, result, *rest = line.split(',')
        
        if home_team == "HomeTeam":
            return

        date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y/%m/%d")

        if result == 'D':            
            yield home_team, (date, 1)
            yield away_team, (date, 1)
        elif result == 'H':
            yield home_team, (date, 3)
            yield away_team, (date, 0)
        else:
            yield home_team, (date, 0)
            yield away_team, (date, 3)

    def reducer_score(self, team, scores):
        scores = list(scores)
        scores = [s for date, s in scores]
        recent_five_scores = scores[-5:]
        recent_five_scores.reverse()
        yield None, (team, sum(scores), recent_five_scores)

    def reducer_ranking(self, _, scores):
        yield None, sorted(scores, key=lambda t: t[1], reverse=True)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_score, reducer=self.reducer_score),
            MRStep(reducer=self.reducer_ranking)
        ]

if __name__=='__main__':
    LaLigaRecentPerformance.run()
