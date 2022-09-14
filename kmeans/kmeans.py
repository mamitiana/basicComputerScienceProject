from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from random import uniform
from statistics import mean, pstdev
from typing import TypeVar, Generic, List, Sequence

from data_point import DataPoint

def zscore(originale: Sequence[float]) -> List[float]:
    avg: float = mean(originale)
    std: float = pstdev(originale)

    if std==0 : # return all zeros if there is no variation
        return [0]
    return [ (x- avg)/ std for x in originale]
    

Point = TypeVar("Point" , bound=DataPoint)
class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points: List[Point]
        centroid: DataPoint

    def __init__(self , k:int , points:List[Point]) -> None:
        if k<1 : #kmeans can't do negative or zero
            raise ValueError("k must be > 1")
        self._points: List[Point] = points
        self._zscore_normalize()

        #initialize empty cluster with random centroids
        self._clusters: List[KMeans.Cluster] = []
        for _ in range(k):
            # random points
            rand_point: DataPoint = self._random_point()
            cluster: KMeans.Cluster = KMeans.Cluster( [] , rand_point )
            self._clusters.append(cluster)
        
    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]
    
    #return a particular columns
    def _dimension_slice(self, dimension:int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]
    
    def _zscore_normalize(self)->None:
        zscored: List[ List[float] ] = [  [] for _ in range(len(self._points))]

        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscore(dimension_slice)):
                zscored[index].append(zscore)
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])


    def _random_point(self):
        rand_dimensions: List[float] = []
        for dimensions in range(self._points[0].num_dimensions):
            values: List[float] = self._dimension_slice(dimensions)
            rand_values:float = uniform(min(values) , max(values))
            rand_dimensions.append(rand_values)
        return rand_dimensions

    def _assing_clusters(self) -> None:
        for point in self._points:
            closest: DataPoint = min(self._centroids , key=partial(DataPoint.distance , point))
            idx: int = self._centroids.index(closest)
            cluster: KMeans.Cluster = self._clusters[idx]
            cluster.points.append(point)

    def _generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) ==0:
                continue # keep the same controid 
            means: List[float]= []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [p.dimensions[dimension] for p in cluster.points]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)

    def run(self, max_iterations: int = 100) -> List[KMeans.Cluster]:
        for iteration in range(max_iterations):
            for cluster in self._clusters: # clear all clusters
                cluster.points.clear()
                self._assign_clusters() # find cluster each point is closest to
                old_centroids: List[DataPoint] = deepcopy(self._centroids) # record
                self._generate_centroids() # find new centroids
                if old_centroids == self._centroids: # have centroids moved?
                    print(f"Converged after {iteration} iterations")
                    return self._clusters
        return self._clusters


if __name__ == "__main__":
    point1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    point2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    point3: DataPoint = DataPoint([3.0, 1.5, 2.5])
    kmeans_test: KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    test_clusters: List[KMeans.Cluster] = kmeans_test.run()
    for index, cluster in enumerate(test_clusters):
        print(f"Cluster {index}: {cluster.points}")
