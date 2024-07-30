from scipy.stats import norm
import numpy as np


def find_min_phi_for_N2(mu1, sigma1_sq, mu, sigma, a2, b2, P_threshold, tol=1e-5, max_iter=100):
    """
    Find the lowest phi such that at least x% of N2's distribution
    remains within [a2, b2], or indicate if no solution exists.

    Parameters:
    - mu1: Mean of N1
    - sigma1_sq: Variance of N1
    - mu: Mean shift to be applied before phi
    - sigma: Variance increase for N2
    - a2, b2: Bounds of interval I_2
    - x_percent: Target percentage of the distribution to remain within I_2
    - tol: Tolerance for binary search convergence
    - max_iter: Maximum iterations to prevent infinite loops

    Returns:
    - The lowest phi that satisfies the constraint or indicates no solution.
    """
    def calc_percentage_within_interval(phi):
        mu2 = mu1 + mu + phi
        var2 = sigma1_sq + sigma
        sigma2 = var2**0.5
        return norm.cdf(b2, mu2, sigma2) - norm.cdf(a2, mu2, sigma2)
    
    low, high = 0, 10  # Adjust high as necessary
    best_phi = None
    solution_found = False

    for _ in range(max_iter):
        mid = (low + high) / 2
        if calc_percentage_within_interval(mid) < P_threshold:
            low = mid + tol
        else:
            best_phi = mid  # Found a candidate that satisfies the condition
            high = mid - tol
            solution_found = True

        if high - low < tol:
            break

    # Final check to ensure the solution found actually meets the condition
    if solution_found and calc_percentage_within_interval(best_phi) >= P_threshold:
        return best_phi
    else:
        return -1

if __name__ == "__main__":
    # Example usage
    mu1 = 0.05
    sigma1_sq = 1**2
    mu = 1
    sigma = 0.5**2
    a2, b2 = -1, 2
    x_percent = 0.1

    time = np.random.normal(0.5, np.sqrt(0.05), 1)

    lowest_phi = find_min_phi_for_N2(mu1, sigma1_sq, mu, sigma, a2, b2, x_percent)
    print(f"The lowest phi for N2: {lowest_phi}")