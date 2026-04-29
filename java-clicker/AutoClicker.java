import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.InputEvent;

public class AutoClicker {
    private static int targetX = -1;
    private static int targetY = -1;
    private static boolean isLocationSet = false;

    public static void main(String[] args) {
        // İşletim sisteminin native görünümünü kullan
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {}

        JFrame frame = new JFrame("Java Auto Clicker");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(350, 320);
        frame.setResizable(false);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BoxLayout(mainPanel, BoxLayout.Y_AXIS));
        mainPanel.setBorder(new EmptyBorder(15, 20, 15, 20));

        JLabel titleLabel = new JLabel("Java Auto Clicker");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 22));
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel statusLabel = new JLabel("<html><center>Konum: Seçilmedi<br>Durum: Bekleniyor</center></html>");
        statusLabel.setForeground(Color.DARK_GRAY);
        statusLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        statusLabel.setBorder(new EmptyBorder(10, 0, 15, 0));

        JButton selectBtn = new JButton("🎯 Konum Seç (3 Saniye)");
        selectBtn.setBackground(new Color(59, 130, 246));
        selectBtn.setForeground(Color.WHITE);
        selectBtn.setFocusPainted(false);
        selectBtn.setFont(new Font("Arial", Font.BOLD, 14));
        selectBtn.setAlignmentX(Component.CENTER_ALIGNMENT);
        selectBtn.setMaximumSize(new Dimension(280, 40));

        JPanel inputsPanel = new JPanel(new GridLayout(2, 2, 10, 10));
        inputsPanel.setBorder(new EmptyBorder(15, 0, 15, 0));
        inputsPanel.add(new JLabel("Tıklama Sayısı:"));
        JTextField countField = new JTextField("10");
        countField.setHorizontalAlignment(JTextField.CENTER);
        inputsPanel.add(countField);
        inputsPanel.add(new JLabel("Gecikme (sn):"));
        JTextField delayField = new JTextField("1.0");
        delayField.setHorizontalAlignment(JTextField.CENTER);
        inputsPanel.add(delayField);

        JButton startBtn = new JButton("🚀 Başlat");
        startBtn.setBackground(new Color(16, 185, 129));
        startBtn.setForeground(Color.WHITE);
        startBtn.setFocusPainted(false);
        startBtn.setFont(new Font("Arial", Font.BOLD, 16));
        startBtn.setAlignmentX(Component.CENTER_ALIGNMENT);
        startBtn.setMaximumSize(new Dimension(280, 45));

        selectBtn.addActionListener(e -> {
            selectBtn.setEnabled(false);
            startBtn.setEnabled(false);
            
            new Thread(() -> {
                try {
                    for (int i = 3; i > 0; i--) {
                        int finalI = i;
                        SwingUtilities.invokeLater(() -> statusLabel.setText("<html><center>Durum: Farenizi hedefe götürün... <b>" + finalI + "</b></center></html>"));
                        Thread.sleep(1000);
                    }
                    
                    Point p = MouseInfo.getPointerInfo().getLocation();
                    targetX = p.x;
                    targetY = p.y;
                    isLocationSet = true;
                    
                    SwingUtilities.invokeLater(() -> {
                        statusLabel.setText(String.format("<html><center>Konum: X=%d, Y=%d<br>Durum: <b>Konum Kaydedildi</b></center></html>", targetX, targetY));
                        statusLabel.setForeground(new Color(16, 185, 129));
                        selectBtn.setEnabled(true);
                        startBtn.setEnabled(true);
                    });
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }).start();
        });

        startBtn.addActionListener(e -> {
            if (!isLocationSet) {
                JOptionPane.showMessageDialog(frame, "Lütfen önce bir konum seçin!", "Hata", JOptionPane.ERROR_MESSAGE);
                return;
            }

            int count;
            double delay;
            try {
                count = Integer.parseInt(countField.getText());
                delay = Double.parseDouble(delayField.getText());
                if (count <= 0 || delay < 0) throw new NumberFormatException();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(frame, "Lütfen geçerli sayısal değerler girin.", "Hata", JOptionPane.ERROR_MESSAGE);
                return;
            }

            selectBtn.setEnabled(false);
            startBtn.setEnabled(false);
            statusLabel.setText("<html><center>Durum: <b style='color:#f59e0b;'>Tıklanıyor...</b></center></html>");

            new Thread(() -> {
                try {
                    Robot robot = new Robot();
                    Thread.sleep(500); 

                    for (int i = 0; i < count; i++) {
                        robot.mouseMove(targetX, targetY);
                        robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
                        robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
                        Thread.sleep((long) (delay * 1000));
                    }

                    SwingUtilities.invokeLater(() -> {
                        statusLabel.setText(String.format("<html><center>Konum: X=%d, Y=%d<br>Durum: <b>Tıklama Tamamlandı</b></center></html>", targetX, targetY));
                        selectBtn.setEnabled(true);
                        startBtn.setEnabled(true);
                    });
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }).start();
        });

        mainPanel.add(titleLabel);
        mainPanel.add(statusLabel);
        mainPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        mainPanel.add(selectBtn);
        mainPanel.add(inputsPanel);
        mainPanel.add(Box.createVerticalGlue());
        mainPanel.add(startBtn);

        frame.add(mainPanel);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
