import numpy as np
from scipy import spatial

def calculate_similarity_vectors(vector1, vector2): 
    return 1 - spatial.distance.cosine(vector1.tolist(), vector2.tolist())
