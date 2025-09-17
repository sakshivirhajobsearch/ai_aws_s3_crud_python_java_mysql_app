package com.ai.aws.s3.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.ai.aws.s3.model.S3ObjectRecord;

public class S3Repository {

	private static final String JDBC_URL = "jdbc:mysql://localhost:3306/ai_s3_curd?useSSL=false&allowPublicKeyRetrieval=true";
	private static final String DB_USER = "root";
	private static final String DB_PASSWORD = "admin";

	// Save S3 object (avoid duplicates)
	public boolean saveS3Object(S3ObjectRecord record) {
		String checkQuery = "SELECT object_key FROM s3_objects WHERE object_key = ?";
		String insertQuery = "INSERT INTO s3_objects (object_key, bucket_name, metadata, size, ai_result) VALUES (?, ?, ?, ?, ?)";

		try (Connection conn = getConnection();
				PreparedStatement checkStmt = conn.prepareStatement(checkQuery);
				PreparedStatement insertStmt = conn.prepareStatement(insertQuery)) {

			checkStmt.setString(1, record.getObjectKey());
			ResultSet rs = checkStmt.executeQuery();
			if (rs.next())
				return false; // already exists

			insertStmt.setString(1, record.getObjectKey());
			insertStmt.setString(2, record.getBucketName());
			insertStmt.setString(3, record.getMetadata());
			insertStmt.setLong(4, record.getSize());
			insertStmt.setString(5, record.getAiResult());
			int rowsInserted = insertStmt.executeUpdate();
			return rowsInserted > 0;

		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
	}

	// Get object by key
	public S3ObjectRecord getS3ObjectByKey(String objectKey) {
		String query = "SELECT id, object_key, bucket_name, metadata, size, ai_result, created_at FROM s3_objects WHERE object_key = ?";
		try (Connection conn = getConnection(); PreparedStatement stmt = conn.prepareStatement(query)) {

			stmt.setString(1, objectKey);
			ResultSet rs = stmt.executeQuery();
			if (rs.next()) {
				S3ObjectRecord record = new S3ObjectRecord();
				record.setId(rs.getInt("id"));
				record.setObjectKey(rs.getString("object_key"));
				record.setBucketName(rs.getString("bucket_name"));
				record.setMetadata(rs.getString("metadata"));
				record.setSize(rs.getLong("size"));
				record.setAiResult(rs.getString("ai_result"));
				record.setCreatedAt(rs.getTimestamp("created_at"));
				return record;
			}

		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}

	// Delete object by key
	public boolean deleteS3ObjectByKey(String objectKey) {
		String deleteQuery = "DELETE FROM s3_objects WHERE object_key = ?";
		try (Connection conn = getConnection(); PreparedStatement stmt = conn.prepareStatement(deleteQuery)) {

			stmt.setString(1, objectKey);
			int rowsDeleted = stmt.executeUpdate();
			return rowsDeleted > 0;

		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
	}

	// Fetch all S3 objects
	public List<S3ObjectRecord> findAll() {
		List<S3ObjectRecord> records = new ArrayList<>();
		String query = "SELECT id, object_key, bucket_name, metadata, size, ai_result, created_at FROM s3_objects";
		try (Connection conn = getConnection();
				PreparedStatement stmt = conn.prepareStatement(query);
				ResultSet rs = stmt.executeQuery()) {

			while (rs.next()) {
				S3ObjectRecord record = new S3ObjectRecord();
				record.setId(rs.getInt("id"));
				record.setObjectKey(rs.getString("object_key"));
				record.setBucketName(rs.getString("bucket_name"));
				record.setMetadata(rs.getString("metadata"));
				record.setSize(rs.getLong("size"));
				record.setAiResult(rs.getString("ai_result"));
				record.setCreatedAt(rs.getTimestamp("created_at"));
				records.add(record);
			}

		} catch (SQLException e) {
			e.printStackTrace();
		}
		return records;
	}

	private Connection getConnection() throws SQLException {
		return DriverManager.getConnection(JDBC_URL, DB_USER, DB_PASSWORD);
	}
}