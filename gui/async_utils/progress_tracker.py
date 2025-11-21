"""Progress tracking for Streamlit operations.

Provides visual progress indicators with manual update control.
"""

import streamlit as st


class ProgressTracker:
    """Track progress of operations with Streamlit UI updates.
    
    Simple progress indicator for single operations with manual updates.
    Useful for operations where you control each step.
    """
    
    def __init__(self, total: int, description: str = "Processing"):
        """Initialize progress tracker.
        
        Args:
            total: Total number of items to process
            description: Progress bar description
            
        Example:
            tracker = ProgressTracker(total=5, description="Loading agents")
            for i in range(5):
                # Do work
                tracker.update(status=f"Agent {i+1}")
            tracker.complete()
        """
        self.total = total
        self.current = 0
        self.description = description
        self._progress_bar = st.progress(0.0)
        self._status_text = st.empty()
        self._update_display()
    
    def update(self, increment: int = 1, status: str = ""):
        """Update progress.
        
        Args:
            increment: Number of items completed (default: 1)
            status: Optional custom status message
            
        Example:
            tracker.update(status="Processing AAPL")
        """
        self.current = min(self.current + increment, self.total)
        self._update_display(status)
    
    def set(self, current: int, status: str = ""):
        """Set progress to specific value.
        
        Args:
            current: Current progress value
            status: Optional custom status message
            
        Example:
            tracker.set(3, status="3 of 5 complete")
        """
        self.current = min(current, self.total)
        self._update_display(status)
    
    def _update_display(self, status: str = ""):
        """Update progress bar and status text."""
        progress = self.current / self.total if self.total > 0 else 0
        self._progress_bar.progress(progress)
        
        if status:
            self._status_text.text(f"{self.description}: {status}")
        else:
            self._status_text.text(
                f"{self.description}: {self.current}/{self.total} ({progress:.0%})"
            )
    
    def complete(self, message: str = "Complete!"):
        """Mark operation as complete.
        
        Args:
            message: Completion message to display
            
        Example:
            tracker.complete(message="All agents loaded successfully!")
        """
        self._progress_bar.progress(1.0)
        self._status_text.text(message)
    
    def clear(self):
        """Clear progress indicators from UI.
        
        Removes the progress bar and status text from display.
        
        Example:
            tracker.complete()
            time.sleep(1)
            tracker.clear()  # Remove from UI
        """
        self._progress_bar.empty()
        self._status_text.empty()
