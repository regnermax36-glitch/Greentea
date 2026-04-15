package com.maxregner.maps.ui.components
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
@Composable
fun BinaryGrid(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.fillMaxSize()) {
        val step = 50.dp.toPx()
        val color = Color(0xFF00E5FF).copy(alpha = 0.05f)
        var x = 0f
        while (x < size.width) { drawLine(color, Offset(x, 0f), Offset(x, size.height)); x += step }
        var y = 0f
        while (y < size.height) { drawLine(color, Offset(0f, y), Offset(size.width, y)); y += step }
    }
}
