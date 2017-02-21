/*
 * This file is licensed under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.spark.sql.hive.test

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object SmvTestHive
    extends TestHiveContext(
  new SparkContext(
    System.getProperty("spark.sql.test.master", "local[1]"),
    "TestSQLContext",
    new SparkConf()
      .set("spark.sql.test", "")
      .set("spark.sql.hive.metastore.barrierPrefixes",
        "org.apache.spark.sql.hive.execution.PairSerDe")
      .set("spark.sql.warehouse.dir", TestHiveContext.makeWarehouseDir().toURI.getPath)
      // SPARK-8910
      .set("spark.ui.enabled", "false")),
      false)