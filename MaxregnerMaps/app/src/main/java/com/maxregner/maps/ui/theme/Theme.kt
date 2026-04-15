package com.maxregner.maps.ui.theme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
@Composable
fun MaxregnerMapsTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(primary = Color(0xFF00E5FF), background = Color(0xFF0A0A0A)),
        content = content
    )
}
