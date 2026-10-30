package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Brush
import androidx.compose.material.icons.filled.Checklist
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Functions
import androidx.compose.material.icons.filled.GridView
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.TableChart
import androidx.compose.material.icons.filled.TextFields
import androidx.compose.material.icons.filled.ViewAgenda
import androidx.compose.material.icons.filled.ViewWeek
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.local.entity.NoteEntity
import com.example.model.NoteType
import com.example.ui.theme.NoteJsAmber
import com.example.ui.theme.isAppInDarkTheme
import com.example.viewmodel.NavTab
import com.example.viewmodel.NotesViewModel
import com.example.viewmodel.Screen
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Contenedor de Tres Paneles para PC (Windows / Linux) y Pantallas Grandes
 * inspirado en el diseño limpio de Apple Notes en macOS y la modularidad de Notion.
 *
 * Estructura:
 * - Panel Izquierdo (250dp): Carpetas con icono #f59e0b, contadores y engranaje de Ajustes al fondo.
 * - Panel Central (300dp): Buscador, conmutador de vista Grid/Lista por iconos y tarjetas de notas.
 * - Panel Derecho (weight 1f): Lienzo de editor con barra de formato superior estilo macOS (DesktopFormatBar).
 * - Modo Concentración (isFocusMode): Al activarse con el botón ☰, colapsa los dos paneles izquierdos
 *   y expande el editor al 100% del ancho de ventana.
 */
@Composable
fun DesktopMainScaffold(
    viewModel: NotesViewModel,
    modifier: Modifier = Modifier
) {
    var isFocusMode by rememberSaveable { mutableStateOf(false) }
    var isGridView by rememberSaveable { mutableStateOf(false) }
    var searchQuery by rememberSaveable { mutableStateOf("") }

    val currentScreen by viewModel.currentScreen.collectAsStateWithLifecycle()
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    val isDark = isAppInDarkTheme()
    val amberColor = Color(0xFFF59E0B)
    val panelBgLeft = if (isDark) Color(0xFF16181D) else Color(0xFFF3F4F6)
    val panelBgCenter = if (isDark) Color(0xFF121418) else Color(0xFFFAFAFA)
    val dividerColor = if (isDark) Color(0xFF262930) else Color(0xFFE5E7EB)

    Row(
        modifier = modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .testTag("desktop_main_scaffold")
    ) {
        // 1 & 2. Animación de paneles izquierdos según Modo Concentración (isFocusMode)
        AnimatedVisibility(
            visible = !isFocusMode,
            enter = slideInHorizontally(animationSpec = tween(240)) { -it } + fadeIn(tween(200)),
            exit = slideOutHorizontally(animationSpec = tween(240)) { -it } + fadeOut(tween(180))
        ) {
            Row(modifier = Modifier.fillMaxHeight()) {
                // PANEL IZQUIERDO: Carpetas (250dp fijos) + Ajustes anclado al fondo
                Surface(
                    color = panelBgLeft,
                    modifier = Modifier
                        .width(250.dp)
                        .fillMaxHeight()
                        .testTag("desktop_panel_folders")
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .statusBarsPadding()
                            .padding(14.dp)
                    ) {
                        // Barra superior del panel de carpetas con botón ☰ y Nueva Nota
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                IconButton(
                                    onClick = { isFocusMode = true },
                                    modifier = Modifier.size(34.dp).testTag("desktop_focus_mode_btn_left")
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Menu,
                                        contentDescription = "Activar modo concentración",
                                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(
                                    text = "Carpetas",
                                    style = MaterialTheme.typography.titleMedium.copy(
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 16.sp
                                    ),
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }

                            IconButton(
                                onClick = {
                                    viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
                                },
                                modifier = Modifier
                                    .size(32.dp)
                                    .clip(CircleShape)
                                    .background(amberColor)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Add,
                                    contentDescription = "Nueva Nota",
                                    tint = Color.Black,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        // Lista scrolleable de carpetas y colecciones
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .verticalScroll(rememberScrollState()),
                            verticalArrangement = Arrangement.spacedBy(4.dp)
                        ) {
                            Text(
                                text = "COLECCIONES",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 10.5.sp,
                                    letterSpacing = 0.8.sp
                                ),
                                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                            )

                            DesktopFolderRow(
                                title = "Todas las notas",
                                count = uiState.allActiveNotesCount,
                                isSelected = uiState.selectedFolder == null && uiState.activeTab == NavTab.NOTES,
                                amberColor = amberColor,
                                onClick = {
                                    viewModel.setActiveTab(NavTab.NOTES)
                                    viewModel.selectFolder(null)
                                    viewModel.selectTag(null)
                                }
                            )

                            DesktopFolderRow(
                                title = "Notas fijadas",
                                count = uiState.activeNotes.count { it.isPinned },
                                isSelected = false,
                                amberColor = amberColor,
                                onClick = {
                                    viewModel.setActiveTab(NavTab.NOTES)
                                    viewModel.selectFolder(null)
                                }
                            )

                            Spacer(modifier = Modifier.height(10.dp))

                            Text(
                                text = "MIS CARPETAS",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 10.5.sp,
                                    letterSpacing = 0.8.sp
                                ),
                                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                            )

                            val customFolders = uiState.availableFolders.filter {
                                !it.equals("Notas", ignoreCase = true) && !it.equals("Todas", ignoreCase = true)
                            }

                            if (customFolders.isEmpty()) {
                                listOf("Personal", "Trabajo", "Universidad", "Ideas").forEach { folder ->
                                    DesktopFolderRow(
                                        title = folder,
                                        count = uiState.folderNoteCounts[folder] ?: 0,
                                        isSelected = uiState.selectedFolder == folder,
                                        amberColor = amberColor,
                                        onClick = {
                                            viewModel.setActiveTab(NavTab.NOTES)
                                            viewModel.selectFolder(folder)
                                        }
                                    )
                                }
                            } else {
                                customFolders.forEach { folder ->
                                    DesktopFolderRow(
                                        title = folder,
                                        count = uiState.folderNoteCounts[folder] ?: 0,
                                        isSelected = uiState.selectedFolder == folder,
                                        amberColor = amberColor,
                                        onClick = {
                                            viewModel.setActiveTab(NavTab.NOTES)
                                            viewModel.selectFolder(folder)
                                        }
                                    )
                                }
                            }
                        }

                        // Botón de engranaje (Ajustes) anclado en la parte inferior
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .clickable { viewModel.navigateTo(Screen.Settings) }
                                .padding(horizontal = 10.dp, vertical = 10.dp),
                            contentAlignment = Alignment.CenterStart
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(10.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Settings,
                                    contentDescription = "Ajustes",
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(19.dp)
                                )
                                Text(
                                    text = "Ajustes de PC",
                                    style = MaterialTheme.typography.bodyMedium.copy(
                                        fontWeight = FontWeight.Medium,
                                        fontSize = 13.5.sp
                                    ),
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }
                        }
                    }
                }

                VerticalDivider(color = dividerColor, thickness = 1.dp)

                // PANEL CENTRAL: Galería / Lista de Notas (300dp fijos)
                Surface(
                    color = panelBgCenter,
                    modifier = Modifier
                        .width(300.dp)
                        .fillMaxHeight()
                        .testTag("desktop_panel_notes_list")
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .statusBarsPadding()
                            .padding(horizontal = 12.dp, vertical = 10.dp)
                    ) {
                        // Encabezado con conmutador de vista de notas por iconos
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = uiState.selectedFolder ?: "Todas las notas",
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 15.sp
                                ),
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                modifier = Modifier.weight(1f)
                            )

                            // Conmutador de vista solo con iconos (Keep Grid / Lista iOS)
                            Row(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (isDark) Color(0xFF1E2128) else Color(0xFFE5E7EB))
                                    .padding(2.dp),
                                horizontalArrangement = Arrangement.spacedBy(2.dp)
                            ) {
                                IconButton(
                                    onClick = { isGridView = true },
                                    modifier = Modifier
                                        .size(28.dp)
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(if (isGridView) amberColor else Color.Transparent)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.GridView,
                                        contentDescription = "Vista Cuadrícula",
                                        tint = if (isGridView) Color.Black else MaterialTheme.colorScheme.onSurfaceVariant,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                                IconButton(
                                    onClick = { isGridView = false },
                                    modifier = Modifier
                                        .size(28.dp)
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(if (!isGridView) amberColor else Color.Transparent)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.ViewAgenda,
                                        contentDescription = "Vista Lista",
                                        tint = if (!isGridView) Color.Black else MaterialTheme.colorScheme.onSurfaceVariant,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(10.dp))

                        // Buscador de notas
                        OutlinedTextField(
                            value = searchQuery,
                            onValueChange = { searchQuery = it },
                            placeholder = { Text("Buscar...", fontSize = 12.5.sp) },
                            leadingIcon = {
                                Icon(
                                    Icons.Default.Search,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp),
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            },
                            singleLine = true,
                            colors = TextFieldDefaults.colors(
                                focusedContainerColor = if (isDark) Color(0xFF1A1D23) else Color.White,
                                unfocusedContainerColor = if (isDark) Color(0xFF1A1D23) else Color.White,
                                focusedIndicatorColor = amberColor,
                                unfocusedIndicatorColor = dividerColor
                            ),
                            shape = RoundedCornerShape(8.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(46.dp)
                        )

                        Spacer(modifier = Modifier.height(10.dp))

                        // Lista scrolleable de tarjetas de notas
                        val filteredNotes = remember(uiState.activeNotes, searchQuery) {
                            if (searchQuery.isBlank()) {
                                uiState.activeNotes
                            } else {
                                uiState.activeNotes.filter { note ->
                                    note.title.contains(searchQuery, ignoreCase = true) ||
                                            note.content.contains(searchQuery, ignoreCase = true)
                                }
                            }
                        }

                        if (filteredNotes.isEmpty()) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .weight(1f),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "Sin notas disponibles",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 13.sp
                                )
                            }
                        } else {
                            LazyColumn(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .weight(1f),
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                                contentPadding = PaddingValues(bottom = 16.dp)
                            ) {
                                items(filteredNotes, key = { it.id }) { note ->
                                    val isSelected = currentScreen is Screen.Editor && (currentScreen as Screen.Editor).noteId == note.id
                                    DesktopNoteCard(
                                        note = note,
                                        isSelected = isSelected,
                                        amberColor = amberColor,
                                        isDark = isDark,
                                        onClick = {
                                            viewModel.navigateTo(
                                                Screen.Editor(
                                                    noteId = note.id,
                                                    initialType = runCatching { NoteType.valueOf(note.noteType) }.getOrDefault(NoteType.TEXT)
                                                )
                                            )
                                        }
                                    )
                                }
                            }
                        }
                    }
                }

                VerticalDivider(color = dividerColor, thickness = 1.dp)
            }
        }

        // PANEL DERECHO: Lienzo del Editor (ocupa el resto weight(1f), o 100% en Modo Concentración)
        Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.surface)
                .testTag("desktop_panel_editor_canvas")
        ) {
            // 3. BARRA SUPERIOR DE FORMATO macOS (DesktopFormatBar)
            DesktopFormatBar(
                isFocusMode = isFocusMode,
                onToggleFocusMode = { isFocusMode = !isFocusMode },
                amberColor = amberColor,
                onInsertChecklist = {
                    viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.CHECKLIST))
                },
                onInsertKanban = {
                    val screen = currentScreen
                    if (screen !is Screen.Editor) {
                        viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
                    }
                },
                onInsertTable = {
                    val screen = currentScreen
                    if (screen !is Screen.Editor) {
                        viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
                    }
                },
                onInsertKatex = {
                    val screen = currentScreen
                    if (screen !is Screen.Editor) {
                        viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.MATH))
                    }
                },
                onInsertDrawing = {
                    viewModel.navigateTo(Screen.Drawing(noteId = 0L))
                },
                onInsertCallout = {
                    val screen = currentScreen
                    if (screen !is Screen.Editor) {
                        viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
                    }
                }
            )

            // Contenido del Editor en el Lienzo
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
            ) {
                when (val screen = currentScreen) {
                    is Screen.Editor -> {
                        NoteEditorScreen(
                            noteId = screen.noteId,
                            initialType = screen.initialType,
                            initialOpenVoiceDictation = screen.openVoiceDictation,
                            initialOpenDocumentScanner = screen.openDocumentScanner,
                            initialSharedText = screen.initialSharedText,
                            initialSharedTitle = screen.initialSharedTitle,
                            viewModel = viewModel
                        )
                    }
                    is Screen.Drawing -> {
                        DrawingScreen(
                            noteId = screen.noteId,
                            viewModel = viewModel
                        )
                    }
                    is Screen.Settings -> {
                        SettingsScreen(viewModel = viewModel)
                    }
                    else -> {
                        // Si no hay nota seleccionada, muestra el editor listo para nueva nota o la primera
                        val firstNote = uiState.activeNotes.firstOrNull { !it.isLocked }
                        NoteEditorScreen(
                            noteId = firstNote?.id ?: 0L,
                            initialType = NoteType.TEXT,
                            viewModel = viewModel
                        )
                    }
                }
            }
        }
    }
}

/**
 * Fila de carpeta con icono #f59e0b y contador tabular.
 */
@Composable
private fun DesktopFolderRow(
    title: String,
    count: Int,
    isSelected: Boolean,
    amberColor: Color,
    onClick: () -> Unit
) {
    val bgColor = if (isSelected) amberColor.copy(alpha = 0.15f) else Color.Transparent

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(bgColor)
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Default.Folder,
            contentDescription = null,
            tint = amberColor,
            modifier = Modifier.size(18.dp)
        )
        Spacer(modifier = Modifier.width(10.dp))
        Text(
            text = title,
            style = MaterialTheme.typography.bodyMedium.copy(
                fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                fontSize = 13.5.sp
            ),
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        if (count > 0) {
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.labelSmall.copy(
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 11.sp
                ),
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

/**
 * Tarjeta de nota en el Panel Central (Galería / Lista).
 */
@Composable
private fun DesktopNoteCard(
    note: NoteEntity,
    isSelected: Boolean,
    amberColor: Color,
    isDark: Boolean,
    onClick: () -> Unit
) {
    val cardBg = if (isDark) Color(0xFF181B22) else Color.White
    val borderColor = if (isSelected) amberColor else if (isDark) Color(0xFF282C36) else Color(0xFFE5E7EB)
    val dateStr = remember(note.updatedAt) {
        SimpleDateFormat("dd MMM", Locale.getDefault()).format(Date(note.updatedAt))
    }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(cardBg)
            .border(
                width = if (isSelected) 1.5.dp else 1.dp,
                color = borderColor,
                shape = RoundedCornerShape(10.dp)
            )
            .clickable(onClick = onClick)
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            text = note.title.ifBlank { "Sin título" },
            style = MaterialTheme.typography.titleSmall.copy(
                fontWeight = FontWeight.Bold,
                fontSize = 14.sp
            ),
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )

        Text(
            text = note.content.ifBlank { "Nota vacía..." },
            style = MaterialTheme.typography.bodySmall.copy(
                fontSize = 12.sp,
                lineHeight = 16.sp
            ),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = note.folder.ifBlank { "General" },
                style = MaterialTheme.typography.labelSmall.copy(
                    fontSize = 10.5.sp,
                    color = amberColor,
                    fontWeight = FontWeight.SemiBold
                )
            )
            Text(
                text = dateStr,
                style = MaterialTheme.typography.labelSmall.copy(
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.5.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                )
            )
        }
    }
}

/**
 * 3. Barra Superior de Formato macOS (DesktopFormatBar):
 * Botones: tipografía Aa, Checklists, Kanban, Tablas de Propiedades, Ecuaciones KaTeX, Lienzo de Dibujo y Callouts.
 */
@Composable
fun DesktopFormatBar(
    isFocusMode: Boolean,
    onToggleFocusMode: () -> Unit,
    amberColor: Color,
    onInsertChecklist: () -> Unit,
    onInsertKanban: () -> Unit,
    onInsertTable: () -> Unit,
    onInsertKatex: () -> Unit,
    onInsertDrawing: () -> Unit,
    onInsertCallout: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = isAppInDarkTheme()
    val barBg = if (isDark) Color(0xFF16181E) else Color(0xFFF9FAFB)
    val borderColor = if (isDark) Color(0xFF262932) else Color(0xFFE5E7EB)
    var showTypeMenu by remember { mutableStateOf(false) }

    Surface(
        color = barBg,
        modifier = modifier
            .fillMaxWidth()
            .height(48.dp)
            .border(width = 1.dp, color = borderColor)
            .testTag("desktop_format_bar")
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Grupo de botones principales de inserción y formato
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                // Botón ☰ para alternar Modo Concentración
                IconButton(
                    onClick = onToggleFocusMode,
                    modifier = Modifier
                        .size(34.dp)
                        .clip(RoundedCornerShape(6.dp))
                        .background(if (isFocusMode) amberColor.copy(alpha = 0.18f) else Color.Transparent)
                        .testTag("desktop_toggle_focus_mode_btn")
                ) {
                    Icon(
                        imageVector = Icons.Default.Menu,
                        contentDescription = if (isFocusMode) "Salir de modo concentración" else "Activar modo concentración",
                        tint = if (isFocusMode) amberColor else MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(19.dp)
                    )
                }

                Box(modifier = Modifier.width(1.dp).height(20.dp).background(borderColor))

                // Menú de tipografía Aa
                Box {
                    FormatIconButton(
                        label = "Aa",
                        isTextIcon = true,
                        tooltip = "Tipografía y Encabezados",
                        onClick = { showTypeMenu = true }
                    )
                    DropdownMenu(
                        expanded = showTypeMenu,
                        onDismissRequest = { showTypeMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Título (H1)", fontWeight = FontWeight.Bold, fontSize = 16.sp) },
                            onClick = { showTypeMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Encabezado (H2)", fontWeight = FontWeight.SemiBold, fontSize = 14.sp) },
                            onClick = { showTypeMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Subencabezado (H3)", fontSize = 13.sp) },
                            onClick = { showTypeMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Cuerpo (Normal)", fontSize = 13.sp) },
                            onClick = { showTypeMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Monoespaciado", fontFamily = FontFamily.Monospace, fontSize = 12.sp) },
                            onClick = { showTypeMenu = false }
                        )
                    }
                }

                // Checklists
                FormatIconButton(
                    icon = Icons.Default.Checklist,
                    tooltip = "Lista de Verificación",
                    onClick = onInsertChecklist
                )

                // Kanban (Tablero con columnas de estado)
                FormatIconButton(
                    icon = Icons.Default.ViewWeek,
                    tooltip = "Tablero Kanban Notion",
                    onClick = onInsertKanban
                )

                // Tablas de Propiedades
                FormatIconButton(
                    icon = Icons.Default.TableChart,
                    tooltip = "Tabla de Propiedades Notion",
                    onClick = onInsertTable
                )

                // Ecuaciones KaTeX
                FormatIconButton(
                    icon = Icons.Default.Functions,
                    tooltip = "Ecuación KaTeX",
                    onClick = onInsertKatex
                )

                // Lienzo de Dibujo
                FormatIconButton(
                    icon = Icons.Default.Brush,
                    tooltip = "Dibujo Libre",
                    onClick = onInsertDrawing
                )

                // Callouts
                FormatIconButton(
                    icon = Icons.Default.Lightbulb,
                    tooltip = "Nota Destacada / Callout",
                    onClick = onInsertCallout
                )
            }

            // Indicador de modo concentración a la derecha
            if (isFocusMode) {
                Surface(
                    color = amberColor.copy(alpha = 0.16f),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = "Modo Concentración (☰ para restaurar)",
                        color = amberColor,
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun FormatIconButton(
    icon: ImageVector? = null,
    label: String? = null,
    isTextIcon: Boolean = false,
    tooltip: String,
    onClick: () -> Unit
) {
    IconButton(
        onClick = onClick,
        modifier = Modifier
            .size(34.dp)
            .clip(RoundedCornerShape(6.dp))
    ) {
        if (isTextIcon && label != null) {
            Text(
                text = label,
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp
                ),
                color = MaterialTheme.colorScheme.onSurface
            )
        } else if (icon != null) {
            Icon(
                imageVector = icon,
                contentDescription = tooltip,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(18.dp)
            )
        }
    }
}
