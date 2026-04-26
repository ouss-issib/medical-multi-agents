import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/consultation_provider.dart';
import '3_physician_review_screen.dart';

class PatientQAScreen extends StatefulWidget {
  const PatientQAScreen({super.key});

  @override
  State<PatientQAScreen> createState() => _PatientQAScreenState();
}

class _PatientQAScreenState extends State<PatientQAScreen> {
  final TextEditingController _answerController = TextEditingController();

  @override
  void dispose() {
    _answerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<ConsultationProvider>(context);
    final messages = provider.currentState?.messages ?? [];
    final questionCount = provider.currentState?.questionCount ?? 0;
    final isDone = questionCount >= 5;

    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Text('Interrogatoire IA ($questionCount/5)'),
        backgroundColor: const Color(0xFF004D40),
        elevation: 0,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                final isHuman = msg['type'] == 'human';

                // On ignore le tout premier message humain (symptôme initial) pour la clarté du chat
                if (index == 0 && isHuman) return const SizedBox.shrink();

                return ChatBubble(message: msg['content'] ?? '', isMe: isHuman);
              },
            ),
          ),
          if (provider.isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(color: Color(0xFF00796B)),
            ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, -5),
                ),
              ],
            ),
            child: isDone
                ? SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton.icon(
                      icon: const Icon(
                        Icons.medical_services,
                        color: Colors.white,
                      ),
                      label: const Text(
                        "Passer à la revue médecin",
                        style: TextStyle(color: Colors.white, fontSize: 16),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF004D40),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(25),
                        ),
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const PhysicianReviewScreen(),
                          ),
                        );
                      },
                    ),
                  )
                : Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _answerController,
                          decoration: InputDecoration(
                            hintText: "Réponse du patient...",
                            filled: true,
                            fillColor: const Color(0xFFF5F7FA),
                            contentPadding: const EdgeInsets.symmetric(
                              horizontal: 20,
                              vertical: 14,
                            ),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(30),
                              borderSide: BorderSide.none,
                            ),
                          ),
                          onSubmitted: (_) => _submitAnswer(provider),
                        ),
                      ),
                      const SizedBox(width: 10),
                      CircleAvatar(
                        backgroundColor: const Color(0xFF00796B),
                        radius: 25,
                        child: IconButton(
                          icon: const Icon(Icons.send, color: Colors.white),
                          onPressed: () => _submitAnswer(provider),
                        ),
                      ),
                    ],
                  ),
          ),
        ],
      ),
    );
  }

  void _submitAnswer(ConsultationProvider provider) async {
    final text = _answerController.text.trim();
    if (text.isNotEmpty && !provider.isLoading) {
      _answerController.clear();
      await provider.submitPatientAnswer(text);
    }
  }
}

// Composant visuel pour les bulles de chat
class ChatBubble extends StatelessWidget {
  final String message;
  final bool isMe;

  const ChatBubble({super.key, required this.message, required this.isMe});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
        decoration: BoxDecoration(
          color: isMe ? const Color(0xFF00796B) : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(20),
            topRight: const Radius.circular(20),
            bottomLeft: Radius.circular(isMe ? 20 : 0),
            bottomRight: Radius.circular(isMe ? 0 : 20),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.04),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Text(
          message,
          style: TextStyle(
            color: isMe ? Colors.white : Colors.black87,
            fontSize: 15,
            height: 1.4,
          ),
        ),
      ),
    );
  }
}
