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

package org.tresamigos.smv

import dqm.DqmValidationResult

class SmvRunInfoCollectorSpec extends SmvUnitSpec {
  "SmvRunInfoCollector" should "store validation results per dataset" in {
    val target = new SmvRunInfoCollector
    val r1 = new DqmValidationResult(true, null)
    target.addRunInfo("a", r1, null, null)

    target.getDqmValidationResult("a") shouldBe r1
  }

  it should "throw when asked for a non-existent validation result" in {
    val target = new SmvRunInfoCollector
    intercept[SmvRuntimeException] {
      target.getDqmValidationResult("a")
    }
  }

  it should "store only the last validation result for a given dataset" in {
    val target = new SmvRunInfoCollector
    val r1 = new DqmValidationResult(true, null)
    val r2 = new DqmValidationResult(false, null)
    target.addRunInfo("a", r1, null, null)
    target.addRunInfo("a", r2, null, null)

    target.getDqmValidationResult("a") shouldBe r2
  }

  it should "keep all datasets for which there is a validation result" in {
    val target = new SmvRunInfoCollector
    target.addRunInfo("a", new DqmValidationResult(true, null), null, null)
    target.addRunInfo("b", new DqmValidationResult(false, null), null, null)
    target.addRunInfo("c", new DqmValidationResult(false, null), null, null)

    target.dsFqns shouldBe Set("a", "b", "c")
  }

  it should "not accept null for dataset fqn" in {
    val target = new SmvRunInfoCollector
    intercept[IllegalArgumentException] {
      target.addRunInfo(null, new DqmValidationResult(true, null), null, null)
    }
  }

  it should "not accept empty string for dataset fqn" in {
    val target = new SmvRunInfoCollector
    intercept[IllegalArgumentException] {
      target.addRunInfo("", new DqmValidationResult(true, null), null, null)
    }
  }
}
