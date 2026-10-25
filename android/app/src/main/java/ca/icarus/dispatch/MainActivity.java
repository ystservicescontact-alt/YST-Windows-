package ca.icarus.dispatch;

import android.os.Bundle;
import androidx.activity.EdgeToEdge;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Draw behind the status bar; the page keeps its content clear of it (viewport-fit=cover).
        EdgeToEdge.enable(this);
        super.onCreate(savedInstanceState);
    }
}
