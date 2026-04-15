package com.maxregner.maps

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.maxregner.maps.ui.components.*
import com.maxregner.maps.ui.theme.MaxregnerMapsTheme
import com.maxregner.maps.data.OfflineMapManager

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val offlineManager = OfflineMapManager(this)
        setContent {
            MaxregnerMapsTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        MapLibreView(modifier = Modifier.fillMaxSize())
                        BinaryGrid(modifier = Modifier.fillMaxSize())
                        ServiceModeOverlay(modifier = Modifier.align(Alignment.TopStart))

                        Button(
                            onClick = { offlineManager.downloadGermany() },
                            modifier = Modifier.align(Alignment.BottomEnd).padding(24.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00E5FF).copy(alpha = 0.7f))
                        ) {
                            Text("DOWNLOAD GERMANY", color = Color.Black)
                        }
                    }
                }
            }
        }
    }
}
