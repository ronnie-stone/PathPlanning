from scipy.stats import norm

def find_max_phi_for_N1(mu1, sigma1, a1, b1, x_percent, tw_min, tol=1e-5, max_iter=100):
    """
    Find the largest phi such that at least x% of N1's distribution
    remains within [a1, b1] after shifting N1 by phi.

    Parameters:
    - mu1: Mean of N1
    - sigma1: Standard deviation of N1
    - a1, b1: Bounds of interval I_1
    - x_percent: Target percentage of the distribution to remain within I_1
    - tol: Tolerance for binary search convergence
    - max_iter: Maximum iterations to prevent infinite loops

    Returns:
    - The largest phi that satisfies the constraint.
    """
    # Define the function to calculate the percentage of N1 within [a1, b1] after shifting by phi
    def calc_percentage_within_interval(phi):
        shifted_mu1 = mu1 + phi
        return norm.cdf(b1, loc=shifted_mu1, scale=sigma1) - norm.cdf(a1, loc=shifted_mu1, scale=sigma1)
    
    # Initialize binary search bounds
    low, high = tw_min, 10  # Adjust the high bound as necessary to ensure it's sufficiently large
    best_phi = None  # Initialize best_phi in case x_percent is already not satisfied even without shifting
    solution_found = False

    for _ in range(max_iter):
        mid = (low + high) / 2
        if calc_percentage_within_interval(mid) >= x_percent / 100.0:
            best_phi = mid  # Update best_phi if the current mid satisfies the constraint
            low = mid + tol  # Move the lower bound up, since we're looking for the largest phi
            solution_found = True
        else:
            high = mid - tol  # Move the upper bound down

        if high - low < tol:  # Convergence criterion
            break

    if solution_found and calc_percentage_within_interval(best_phi) >= x_percent / 100.0:
        return best_phi
    else:
        return -1

# Example usage
mu1 = 0  # Example mean
sigma1 = 1  # Example standard deviation
a1, b1 = -1, 1  # Example interval bounds
x_percent = 68  # Example percentage

largest_phi = find_max_phi_for_N1(mu1, sigma1, a1, b1, x_percent, 0)
print(f"The largest phi for N1: {largest_phi}")