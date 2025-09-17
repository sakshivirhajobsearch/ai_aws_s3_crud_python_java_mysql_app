package com.ai.aws.s3.model;

import java.sql.Timestamp;

public class S3ObjectRecord {

	private int id; // unique ID
	private String objectKey;
	private String bucketName;
	private String metadata;
	private Timestamp createdAt;
	private long size; // S3 object size
	private String aiResult; // AI analysis result

	public S3ObjectRecord() {
	}

	// Getters & Setters
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getObjectKey() {
		return objectKey;
	}

	public void setObjectKey(String objectKey) {
		this.objectKey = objectKey;
	}

	public String getBucketName() {
		return bucketName;
	}

	public void setBucketName(String bucketName) {
		this.bucketName = bucketName;
	}

	public String getMetadata() {
		return metadata;
	}

	public void setMetadata(String metadata) {
		this.metadata = metadata;
	}

	public Timestamp getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(Timestamp createdAt) {
		this.createdAt = createdAt;
	}

	public long getSize() {
		return size;
	}

	public void setSize(long size) {
		this.size = size;
	}

	public String getAiResult() {
		return aiResult;
	}

	public void setAiResult(String aiResult) {
		this.aiResult = aiResult;
	}
}