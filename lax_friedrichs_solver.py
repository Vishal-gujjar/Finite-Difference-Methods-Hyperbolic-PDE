import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

def solve_wave_equation_corrected():
    """
    CORRECTED implementation with proper zero-gradient boundary conditions
    """
    # Domain parameters
    L = 2.0  # x ∈ [-1, 1]
    Nx = 2000
    T = 1.5
    dx = L / Nx
    x = np.linspace(-1, 1, Nx+1)
    
    # CFL condition - use more restrictive condition
    dt = 0.8*dx # More stable
    
    # Initial conditions
    rho = np.zeros(Nx+1)
    u = np.zeros(Nx+1)
    
    rho[x <= 0] = 0.1
    rho[x > 0] = 10.0
    u[x <= 0] = 2.0
    u[x > 0] = 1.0
    
    # Store solution
    rho_history = [rho.copy()]
    u_history = [u.copy()]
    times = [0.0]
    
    total_steps = int(T / dt) + 1  # how many time steps your simulation will run
    store_every = max(1, total_steps // 100)
    
    print("CORRECTED IMPLEMENTATION:")
    print("Proper zero-gradient boundary conditions")
    
    t = 0.0
    step = 0
    
    while t < T:
        rho_new = np.zeros(Nx+1)
        u_new = np.zeros(Nx+1)
        

        # PROPER BOUNDARY CONDITION: Set ghost cells FIRST
        # For zero-gradient: ghost cells = boundary values
        
        rho_left_ghost = rho[0]    # Q_{-1} = Q_0
        rho_right_ghost = rho[-1]  # Q_{N} = Q_{N-1}  
        u_left_ghost = u[0]
        u_right_ghost = u[-1]
        
        
        # Reflective BC: mirror the value across the boundary
        """
        rho_left_ghost  = rho[1]   # reflection symmetric for scalar
        rho_right_ghost = rho[-2]
        u_left_ghost    = -u[1]    # reverse sign (velocity reverses at wall)
        u_right_ghost   = -u[-2]
        """


        # Lax-Friedrichs scheme for ALL points including boundaries
        for i in range(Nx+1):
            if i == 0:  # Left boundary
                rho_new[i] = 0.5 * (rho[1] + rho_left_ghost) - 0.5 * (dt/dx) * (u[1] - u_left_ghost)
                u_new[i] = 0.5 * (u[1] + u_left_ghost) - 0.5 * (dt/dx) * (rho[1] - rho_left_ghost)
            elif i == Nx:  # Right boundary  
                rho_new[i] = 0.5 * (rho_right_ghost + rho[-2]) - 0.5 * (dt/dx) * (u_right_ghost - u[-2])
                u_new[i] = 0.5 * (u_right_ghost + u[-2]) - 0.5 * (dt/dx) * (rho_right_ghost - rho[-2])
            else:  # Interior points
                rho_new[i] = 0.5 * (rho[i+1] + rho[i-1]) - 0.5 * (dt/dx) * (u[i+1] - u[i-1])
                u_new[i] = 0.5 * (u[i+1] + u[i-1]) - 0.5 * (dt/dx) * (rho[i+1] - rho[i-1])

        rho, u = rho_new, u_new
        t += dt
        step += 1
        
        if step % store_every == 0 or t >= T:
            rho_history.append(rho.copy())
            u_history.append(u.copy())
            times.append(t)
    
    print(f"Solution computed: final t = {t:.3f}")

    final_rho = np.mean(rho)  # Average across domain
    final_u = np.mean(u)      # Average across domain
    
    print("\n" + "="*50)
    print("FINAL SATURATED VALUES (Steady State):")
    print(f"Density: {final_rho:.6f}")
    print(f"Velocity: {final_u:.6f}")
    print("="*50)

    return x, rho_history, u_history, times

def create_corrected_animation():
    """
    Create animation with CORRECT physics
    """
    x, rho_history, u_history, times = solve_wave_equation_corrected()
    
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
    ax1.set_ylim(-1, 12)
    ax2.set_ylim(-4, 2.5)
    
    # Mark boundaries with vertical lines (without legends)
    ax1.axvline(x=-1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax1.axvline(x=1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax2.axvline(x=-1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    ax2.axvline(x=1, color='red', linestyle=':', alpha=0.8, linewidth=2)
    
    # Initial plots
    line_rho, = ax1.plot(x, rho_history[0], 'cyan', linewidth=2.5, alpha=0.9)
    line_u, = ax2.plot(x, u_history[0], 'yellow', linewidth=2.5, alpha=0.9)
    
    # SINGLE MAIN TITLE for the entire figure
    plt.suptitle('Finite Difference Method: Initial Value Problem using the Lax-Friedrichs Scheme', 
                 color='white', fontsize=16, fontweight='bold', y=0.97)
    
    # Information text boxes
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=12,
                        color='white', fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="blue", alpha=0.9, edgecolor='white'))
    
    phase_text = ax1.text(0.75, 0.95, '', transform=ax1.transAxes, fontsize=11,
                         color='white', fontweight='bold', ha='center',
                         bbox=dict(boxstyle="round,pad=0.4", facecolor="green", alpha=0.8, edgecolor='white'))
    
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
            phase = 'WAVE PROPAGATION\nFrom Initial Discontinuity'
            color = 'green'
            boundary_info = 'Zero-gradient BCs active\nWaves approaching boundaries'
        elif t < 1.15:
            phase = 'BOUNDARY INTERACTION\nWaves Reaching x = ±1'
            color = 'orange'
            boundary_info = 'Waves exiting domain\nNon-reflective boundaries'
        else:
            phase = 'STEADY STATE APPROACH\nDomain Stabilizing'
            color = 'blue'
            boundary_info = 'Waves have exited\nZero-gradient maintained'
        
        phase_text.set_text(phase)
        phase_text.set_bbox(dict(boxstyle="round,pad=0.4", facecolor=color, alpha=0.8, edgecolor='white'))
        boundary_text.set_text(boundary_info)
        
        return line_rho, line_u, time_text, phase_text, boundary_text
    
    total_frames = len(rho_history)
    anim = FuncAnimation(fig, animate, frames=total_frames,
                        interval=30, blit=True, repeat=True)
    
    print("Animation created successfully!")
    plt.show()
    
    return anim

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("FINITE DIFFERENCE METHOD - LAX-FRIEDRICHS SCHEME")
    print("Solving Hyperbolic PDE System: ∂ρ/∂t + ∂u/∂x = 0, ∂u/∂t + ∂ρ/∂x = 0")
    print("Domain: x ∈ [-1, 1] with Zero-Gradient Boundary Conditions")
    print("="*70)
    
    anim = create_corrected_animation()
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("• Proper implementation of Lax-Friedrichs scheme")
    print("• Correct zero-gradient boundary conditions")
    print("• Waves exit domain without reflection")
    print("="*70)