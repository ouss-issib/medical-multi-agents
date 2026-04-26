import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/consultation_provider.dart';
import '2_patient_qa_screen.dart';

class InitialCaseScreen extends StatefulWidget {
  const InitialCaseScreen({super.key});

  @override
  State<InitialCaseScreen> createState() => _InitialCaseScreenState();
}

class _InitialCaseScreenState extends State<InitialCaseScreen> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<ConsultationProvider>(context);

    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA), // Fond gris clair
      appBar: AppBar(
        title: const Text(
          'Nouvelle Consultation',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: const Color(0xFF004D40), // Teal Foncé
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Motif de consultation",
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Color(0xFF004D40),
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              "Décrivez brièvement les symptômes initiaux du patient.",
              style: TextStyle(fontSize: 16, color: Colors.black54),
            ),
            const SizedBox(height: 30),
            TextField(
              controller: _controller,
              maxLines: 5,
              decoration: InputDecoration(
                hintText:
                    "Ex: Le patient présente une fièvre et une toux depuis 48h...",
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: const BorderSide(
                    color: Color(0xFF00796B),
                    width: 2,
                  ),
                ),
                contentPadding: const EdgeInsets.all(20),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF004D40),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 2,
                ),
                onPressed: provider.isLoading
                    ? null
                    : () async {
                        if (_controller.text.trim().isNotEmpty) {
                          await provider.startConsultation(_controller.text);
                          if (context.mounted) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => PatientQAScreen(),
                              ),
                            );
                          }
                        }
                      },
                child: provider.isLoading
                    ? const SizedBox(
                        height: 24,
                        width: 24,
                        child: CircularProgressIndicator(
                          color: Colors.white,
                          strokeWidth: 2,
                        ),
                      )
                    : const Text(
                        "Démarrer l'interrogatoire",
                        style: TextStyle(fontSize: 18, color: Colors.white),
                      ),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
