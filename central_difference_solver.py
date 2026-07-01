import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

def solve_wave_equation_central_difference():
    """
    Central Difference Method implementation with proper zero-gradient boundary conditions
    """
    # Domain parameters
    L = 2.0  # x ∈ [-1, 1]
    Nx = 1000
    T = 1.5
    dx = L / (Nx - 1)
    x = np.linspace(-1.0, 1.0, Nx)
    
    # CFL condition - use more restrictive condition for stability
    dt = 0.8*dx  # More conservative for central difference
    
    # Initial conditions
    rho = np.zeros(Nx)
    u = np.zeros(Nx)
    
    rho[x <= 0] = 0.1
    rho[x > 0] = 10.0
    u[x <= 0] = 2.0
    u[x > 0] = 1.0
    
    # Store solution
    rho_history = [rho.copy()]
    u_history = [u.copy()]
    times = [0.0]
    
    total_steps = int(T / dt) + 1
    store_every = max(1, total_steps // 200)
    
    print("CENTRAL DIFFERENCE METHOD IMPLEMENTATION:")
    print("Using scheme: ρ_i^(n+1) = ρ_i^(n) - (Δt/(2Δx)) * [u_(i+1)^(n) - u_(i-1)^(n)]")
    print("              u_i^(n+1) = u_i^(n) - (Δt/(2Δx)) * [ρ_(i+1)^(n) - ρ_(i-1)^(n)]")
    
    t = 0.0
    step = 0
    
    while t < T:
        rho_new = np.zeros(Nx)
        u_new = np.zeros(Nx)
        
        # PROPER BOUNDARY CONDITION: Set ghost cells for central difference
        # For zero-gradient: ghost cells = boundary values
        rho_left_ghost = rho[0]    # Q_{-1} = Q_0
        rho_right_ghost = rho[-1]  # Q_{N} = Q_{N-1}  
        u_left_ghost = u[0]
        u_right_ghost = u[-1]
        
        # Central Difference scheme for ALL points including boundaries
        for i in range(Nx):
            if i == 0:  # Left boundary - use ghost cell
                rho_new[i] = rho[i] - (dt/(2*dx)) * (u[1] - u_left_ghost)
                u_new[i] = u[i] - (dt/(2*dx)) * (rho[1] - rho_left_ghost)
            elif i == Nx-1:  # Right boundary - use ghost cell
                rho_new[i] = rho[i] - (dt/(2*dx)) * (u_right_ghost - u[-2])
                u_new[i] = u[i] - (dt/(2*dx)) * (rho_right_ghost - rho[-2])
            else:  # Interior points - standard central difference
                rho_new[i] = rho[i] - (dt/(2*dx)) * (u[i+1] - u[i-1])
                u_new[i] = u[i] - (dt/(2*dx)) * (rho[i+1] - rho[i-1])
        
        rho, u = rho_new, u_new
        t += dt
        step += 1
        
        if step % store_every == 0 or t >= T:
            rho_history.append(rho.copy())
            u_history.append(u.copy())
            times.append(t)
    
    print(f"Solution computed: final t = {t:.3f}")
    return x, rho_history, u_history, times

def create_central_difference_animation():
    """
    Create animation with Central Difference Method
    """
    x, rho_history, u_history, times = solve_wave_equation_central_difference()
    
    # Create figure with black background
    fig = plt.figure(figsize=(14, 10), facecolor='black')
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    
    # Create subplots
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # Set black background for both subplots
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')
    ax2.set_facecolor('black')
    
    # Configure axes appearance
    for ax in [ax1, ax2]:
        ax.tick_params(colors='white', which='both', labelsize=11)
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(1.5)
        ax.grid(True, alpha=0.3, color='white', linestyle='--')
        ax.set_xlim(-1.0, 1.0)
        ax.set_xlabel('Position (x)', color='white', fontsize=12, fontweight='bold', labelpad=10)
    
    # Set y-axis labels
    ax1.set_ylabel('Density (ρ)', color='cyan', fontsize=12, fontweight='bold', labelpad=10)
    ax2.set_ylabel('Velocity (u)', color='yellow', fontsize=12, fontweight='bold', labelpad=10)
    
    # Set axis limits
    ax1.set_ylim(-5000, 5000)
    ax2.set_ylim(-5000, 5000)
    
    # Mark boundaries with vertical lines
    ax1.axvline(x=-1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax1.axvline(x=1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax2.axvline(x=-1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax2.axvline(x=1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    
    # Initial plots
    line_rho, = ax1.plot(x, rho_history[0], 'cyan', linewidth=2.5, alpha=0.9)
    line_u, = ax2.plot(x, u_history[0], 'yellow', linewidth=2.5, alpha=0.9)
    
    # SINGLE MAIN TITLE for the entire figure
    plt.suptitle('Finite Difference Method: Initial Value Problem using Central Difference Scheme', 
                 color='white', fontsize=16, fontweight='bold', y=0.97)
    
    # Information text boxes
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=12,
                        color='white', fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="blue", alpha=0.9, edgecolor='white'))
    
    method_text = ax1.text(0.75, 0.95, '', transform=ax1.transAxes, fontsize=11,
                          color='white', fontweight='bold', ha='center',
                          bbox=dict(boxstyle="round,pad=0.4", facecolor="purple", alpha=0.8, edgecolor='white'))
    
    boundary_text = ax2.text(0.02, 0.95, '', transform=ax2.transAxes, fontsize=11,
                            color='white', fontweight='bold',
                            bbox=dict(boxstyle="round,pad=0.4", facecolor="red", alpha=0.8, edgecolor='white'))
    
    # Adjust layout to prevent warning
    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.92, hspace=0.3)
    
    def animate(frame):
        current_frame = min(frame, len(rho_history) - 1)
        t = times[current_frame]
        
        # Update waves
        line_rho.set_ydata(rho_history[current_frame])
        line_u.set_ydata(u_history[current_frame])
        
        time_text.set_text(f'TIME: {t:.2f}s')
        
        # Physics description based on time
        if t < 0.75:
            phase = 'CENTRAL DIFFERENCE\nWave Propagation Phase'
            color = 'purple'
            boundary_info = 'Zero-gradient BCs\nCentral difference at boundaries'
        elif t < 1.15:
            phase = 'BOUNDARY INTERACTION\nCentral Scheme Active'
            color = 'orange'
            boundary_info = 'Waves reaching boundaries\nUsing ghost cells'
        else:
            phase = 'SCHEME EVOLUTION\nCentral Difference Method'
            color = 'blue'
            boundary_info = 'Central difference scheme\nin progress'
        
        method_text.set_text(phase)
        method_text.set_bbox(dict(boxstyle="round,pad=0.4", facecolor=color, alpha=0.8, edgecolor='white'))
        boundary_text.set_text(boundary_info)
        
        return line_rho, line_u, time_text, method_text, boundary_text
    
    total_frames = len(rho_history)
    anim = FuncAnimation(fig, animate, frames=total_frames,
                        interval=30, blit=True, repeat=True)
    
    print("Central Difference Animation created successfully!")
    plt.show()
    
    return anim

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("FINITE DIFFERENCE METHOD - CENTRAL DIFFERENCE SCHEME")
    print("Solving Hyperbolic PDE System: ∂ρ/∂t + ∂u/∂x = 0, ∂u/∂t + ∂ρ/∂x = 0")
    print("Using Scheme: ρ_i^(n+1) = ρ_i^(n) - (Δt/(2Δx)) * [u_(i+1)^(n) - u_(i-1)^(n)]")
    print("Domain: x ∈ [-1, 1] with Zero-Gradient Boundary Conditions")
    print("="*70)
    
    anim = create_central_difference_animation()
    
    print("\n" + "="*70)
    print("CENTRAL DIFFERENCE SIMULATION COMPLETED")
    print("• Central Difference Method implementation")
    print("• Same zero-gradient boundary conditions")
    print("• Different numerical characteristics compared to Lax-Friedrichs")
    print("="*70)