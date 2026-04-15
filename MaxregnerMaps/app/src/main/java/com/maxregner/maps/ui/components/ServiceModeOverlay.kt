package com.maxregner.maps.ui.components
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
@Composable
fun ServiceModeOverlay(modifier: Modifier = Modifier) {
    Column(modifier = modifier.padding(16.dp).background(Color(0xCC000000)).padding(8.dp)) {
        Text("MAXREGNER SYSTEM RADAR", color = Color(0xFF00E5FF), fontSize = 10.sp)
        Text("STATUS: ONLINE", color = Color.Green, fontSize = 12.sp)
        Text("PROT: LOKE-X64", color = Color(0xFF7C4DFF), fontSize = 10.sp)
    }
}
