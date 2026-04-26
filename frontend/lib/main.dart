import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'presentation/providers/consultation_provider.dart';
import 'presentation/screens/1_initial_case_screen.dart'; // ✅ Vérifie le chemin

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ConsultationProvider()),
      ],
      child: const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: InitialCaseScreen(), // ✅ Doit correspondre au nom de ta classe
      ),
    ),
  );
}
