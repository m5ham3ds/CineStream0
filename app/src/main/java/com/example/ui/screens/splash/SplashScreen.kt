package com.example.ui.screens.splash

import androidx.compose.animation.core.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.repository.UserPreferencesRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first

@Composable
fun SplashScreen(
    onNavigateToOnboarding: () -> Unit,
    onNavigateToAuth: () -> Unit,
    onNavigateToMain: (String) -> Unit
) {
    val context = LocalContext.current
    val userPrefs = remember { UserPreferencesRepository(context) }
    
    var startAnimation by remember { mutableStateOf(false) }
    val alphaAnim = animateFloatAsState(
        targetValue = if (startAnimation) 1f else 0f,
        animationSpec = tween(durationMillis = 1500),
        label = "alphaAnim"
    )
    
    var verificationText by remember { mutableStateOf("Initializing...") }
    var verificationComplete by remember { mutableStateOf(false) }
    
    val sitesToVerify = remember {
        listOf(
            "https://tv10.egydead.live/", "https://vidsrc.me/", "https://multiembed.mov/", "https://vidsrc.to/",
            "https://egydead.icu/", "https://faselhd.club/", "https://anime4up.com/",
            "https://witanime.com/", "https://cimaleek.com/", "https://asia2tv.cc/",
            "https://tuktukcinema.net/", "https://arabseed-tv.com/", "https://www.arabseed.wine/",
            "https://e.cimalight.co/", "https://egybests.live/", "https://www.stardima.com/",
            "https://a.qfilm.tv/", "https://egydead.rip/", "https://mycima.red/", 
            "https://witanime.you/", "https://animesit.com/"
        )
    }

    com.example.ui.components.BackgroundWebView(
        urls = sitesToVerify,
        onProgress = { url -> 
            val domain = try { java.net.URI(url).host } catch (e: Exception) { url }
            verificationText = "Verifying $domain..."
        },
        onSiteVerified = { com.example.utils.SiteVerificationManager.markSiteVerified(it) },
        onComplete = { verificationComplete = true }
    )

    LaunchedEffect(verificationComplete) {
        startAnimation = true
        if (!verificationComplete) return@LaunchedEffect
        
        val hasSeenOnboarding = userPrefs.onboardingCompleted.first()
        val isGuest = userPrefs.isGuest.first()
        val isLoggedIn = userPrefs.isLoggedIn.first()
        val startScreen = userPrefs.startScreen.first()
        
        delay(500) // Small delay for smooth transition after verification
        
        if (hasSeenOnboarding) {
            if (isGuest || isLoggedIn) {
                onNavigateToMain(startScreen)
            } else {
                onNavigateToAuth()
            }
        } else {
            onNavigateToOnboarding()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        contentAlignment = Alignment.Center
    ) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?q=80&w=1000&auto=format&fit=crop",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize().alpha(0.2f)
        )
        
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            Color.Transparent,
                            Color.Transparent
                        )
                    )
                )
        )

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.alpha(alphaAnim.value)
        ) {
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            colors = listOf(MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.primary)
                        )
                    )
                    .padding(8.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surface),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.PlayArrow,
                    contentDescription = "Logo",
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(50.dp)
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text(
                text = buildAnnotatedString {
                    withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary)) {
                        append("Cine")
                    }
                    withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.onBackground)) {
                        append("Stream")
                    }
                },
                fontSize = 40.sp,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Text(
                text = "Your Cinematic World, Anytime, Anywhere.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 14.sp
            )
        }
        
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 64.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            CircularProgressIndicator(
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(32.dp),
                strokeWidth = 3.dp
            )
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = verificationText,
                color = MaterialTheme.colorScheme.onBackground,
                fontSize = 14.sp
            )
        }
    }
}
