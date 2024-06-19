#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
    
class LaLigaMR(MRJob):
        
    # Mapper: En esta etapa aún no hay clave (_), el valor lo recibimos en la variable line
    def mapper_points(self, _, line):
        #Por cada línea, esta se divide en los campos que forman las columnas
        _, _, _, home_team, away_team, _, _, result, *rest = line.split(',')
        
        # Si es la cabecera no emitimos nada
        if home_team == "HomeTeam":
            return
        
        # Solo emitimos puntos para el equipo visitante
        if result == 'D':            
            yield away_team, 1
        elif result == 'A':
            yield away_team, 3
            
    def combiner_points(self, team, points):
        yield team, sum(points)
            
    def reducer_points(self, team, points):
        yield None, (team, sum(points))
        
    def reducer_classification(self, _, points):
        yield None, sorted(points, key=lambda t: t[1], reverse=True)
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper_points,
                   combiner=self.combiner_points,
                   reducer=self.reducer_points),
            MRStep(reducer=self.reducer_classification)
        ]
         
if __name__=='__main__':
    LaLigaMR.run()
