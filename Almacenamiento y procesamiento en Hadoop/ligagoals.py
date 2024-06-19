#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class LaLigaAnalysis(MRJob):

    def mapper_score(self, _, line):
        _, _, _, home_team, away_team, home_goals, away_goals, result, *rest = line.split(',')
        
        if home_team == "HomeTeam":
            return

        if result in ['D', 'H']: 
            yield home_team, (int(home_goals))
            yield away_team,(int(away_goals))
        else:            
            yield away_team, (int(away_goals))
            yield home_team,(int(home_goals))

    def combiner_score(self, team, goals):
        yield team, sum(goals)
            
    def reducer_score(self, team, goals):
        yield None, (team, sum(goals))
        
    def reducer_score_diff(self, _, teams):
        sorted_teams = sorted(teams, key=lambda t: t[1], reverse=True)
        top_team = sorted_teams[0][0]
        bottom_team = sorted_teams[-1][0]
        score_diff = sorted_teams[0][1] - sorted_teams[-1][1]
        
        match_up = top_team + " vs " + bottom_team
        diff_str = "Diferencia de goles " + str(score_diff)
        
        yield  (match_up , diff_str)
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper_score,
                   combiner=self.combiner_score,
                   reducer=self.reducer_score),
            MRStep(reducer=self.reducer_score_diff)
        ]

if __name__=='__main__':
    LaLigaAnalysis.run()
