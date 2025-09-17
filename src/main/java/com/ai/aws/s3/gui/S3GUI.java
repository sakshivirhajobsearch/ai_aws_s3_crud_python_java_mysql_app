package com.ai.aws.s3.gui;

import java.awt.BorderLayout;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTable;

import com.ai.aws.s3.model.S3ObjectRecord;
import com.ai.aws.s3.repository.S3Repository;

public class S3GUI extends JFrame {

	public S3GUI() {
		setTitle("S3 Object Viewer with AI");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(600, 400);

		try {
			S3Repository repo = new S3Repository();
			List<S3ObjectRecord> records = repo.findAll();
			String[] columns = { "ID", "Object Key", "Size", "AI Result" };
			String[][] data = new String[records.size()][4];

			for (int i = 0; i < records.size(); i++) {
				S3ObjectRecord r = records.get(i);
				data[i][0] = String.valueOf(r.getId());
				data[i][1] = r.getObjectKey();
				data[i][2] = String.valueOf(r.getSize());
				data[i][3] = r.getAiResult();
			}

			JTable table = new JTable(data, columns);
			add(new JScrollPane(table), BorderLayout.CENTER);

		} catch (Exception e) {
			add(new JLabel("Error: " + e.getMessage()), BorderLayout.CENTER);
		}

		setVisible(true);
	}

	public static void main(String[] args) {
		new S3GUI();
	}
}